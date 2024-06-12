import multiprocessing
import os
import time
from typing import Optional

import google.generativeai as genai
import openai
import torch
from fire import Fire
from peft import PeftModel
from pydantic import BaseModel, Extra
from tqdm import tqdm
from transformers import (
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizer,
)
from vllm import LLM, SamplingParams


class SeqToSeqModel(BaseModel, arbitrary_types_allowed=True):
    model_path: str
    model: Optional[PreTrainedModel]
    tokenizer: Optional[PreTrainedTokenizer]
    lora_path: str = ""
    device: str = "cuda"
    load_8bit: bool = False
    max_output_length: int = 1024

    def load(self):
        if self.model is None:
            args = {}
            if self.load_8bit:
                args.update(device_map="auto", load_in_8bit=True)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path, **args)
            if self.lora_path:
                self.model = PeftModel.from_pretrained(self.model, self.lora_path)
            self.model.eval()
            if not self.load_8bit:
                self.model.to(self.device)
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)

    def generate(self, prompt: str, **kwargs) -> str:
        self.load()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=self.max_output_length,
            **kwargs,
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def count_text_length(self, text: str) -> int:
        self.load()
        return len(self.tokenizer(text).input_ids)


class CausalModel(SeqToSeqModel):
    def load(self):
        if self.model is None:
            args = {}
            if self.load_8bit:
                args.update(device_map="auto", load_in_8bit=True)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path, trust_remote_code=True, **args
            )
            self.model.eval()
            if not self.load_8bit:
                self.model.to(self.device)
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path, trust_remote_code=True
            )

    def generate(self, prompt: str, **kwargs) -> str:
        self.load()
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        if "RWForCausalLM" in str(type(self.model)):
            inputs.pop("token_type_ids")  # Not used by Falcon model

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=self.max_output_length,
            pad_token_id=self.tokenizer.eos_token_id,  # Avoid pad token warning
            **kwargs,
        )
        batch_size, length = inputs.input_ids.shape
        return self.tokenizer.decode(outputs[0, length:], skip_special_tokens=True)


class VLLM(BaseModel, arbitrary_types_allowed=True):
    model_path: str
    model: Optional[LLM]
    max_output_length: int = 2048
    loaded: bool = False
    temperature: float = 0.8
    top_p: float = 1.0
    top_k: int = -1
    sampling_params: Optional[SamplingParams]

    def load(self):
        self.sampling_params = SamplingParams(
            temperature=self.temperature,
            max_tokens=self.max_output_length,
            top_p=self.top_p,
            top_k=self.top_k,
        )
        if "awq" in self.model_path.lower():
            self.model = LLM(
                self.model_path,
                quantization="awq",
            )
        else:
            self.model = LLM(
                self.model_path,
            )
        self.loaded = True

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.loaded:
            self.load()

        if "orca" in self.model_path.lower():
            prompt_template = """<|im_start|>system
{system_message}<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
"""
            prompt = (prompt_template.format(prompt=prompt, system_message=""),)

        output = self.model.generate(
            prompt,
            self.sampling_params,
            use_tqdm=False,
            **kwargs,
        )
        return output[0].outputs[0].text


class Llama3(BaseModel, arbitrary_types_allowed=True, extra=Extra.allow):
    model_path: str = "meta-llama/Meta-Llama-3-8B-Instruct"
    model: Optional[LLM] = None
    max_output_length: int = 2048
    loaded: bool = False
    temperature: float = 0.8
    top_p: float = 1.0
    top_k: int = -1
    sampling_params: Optional[SamplingParams] = None

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.terminators = [
            self.tokenizer.eos_token_id,
            self.tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        ]

        # self.pipeline = transformers.pipeline(
        #     "text-generation",
        #     model=self.model_path,
        #     model_kwargs={"torch_dtype": torch.bfloat16},
        #     device_map="auto",
        # )
        # self.sampling_params = SamplingParams(
        #     temperature=self.temperature,
        #     max_tokens=self.max_output_length,
        #     top_p=self.top_p,
        #     top_k=self.top_k,
        #     stop_token_ids=[
        #         tokenizer.eos_token_id,
        #         tokenizer.convert_tokens_to_ids("<|eot_id|>"),
        #     ],
        # )

        self.loaded = True

    def generate(self, prompt: str, **kwargs) -> str:
        if not self.loaded:
            self.load()
        input_ids = self.prepare_prompt(prompt, **kwargs)
        output = self.model.generate(
            input_ids,
            max_new_tokens=self.max_output_length,
            eos_token_id=self.terminators,
            do_sample=True,
            temperature=self.temperature,
            top_p=self.top_p,
            **kwargs,
        )
        response = output[0][input_ids.shape[-1] :]

        return self.tokenizer.decode(response, skip_special_tokens=True)

    def prepare_prompt(self, user_prompt, system_prompt="", **kwargs):
        messages = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": user_prompt},
        ]

        prompt = self.tokenizer.apply_chat_template(
            messages, add_generation_prompt=True, return_tensors="pt"
        ).to(self.model.device)

        return prompt


class GPT4(BaseModel, arbitrary_types_allowed=True):
    temperature: float = 0.0
    version: str = "4"  # 4 or chat
    loaded: bool = False
    model: Optional[str]
    engine: Optional[str]

    def load(self):
        openai.api_type = "azure"
        if self.version == "4":
            self.model = "gpt-4"
            openai.api_base = "https://declaregpt4.openai.azure.com/"
            openai.api_key = os.environ["OPENAIAPI4"]
            self.engine = "GPT4"
        if self.version == "chat":
            self.model = "gpt-3.5-turbo"
            openai.api_base = "https://research.openai.azure.com/"
            openai.api_key = os.environ["OPENAIAPIchat"]
            self.engine = "Pengfei"
        # openai.api_version = "2023-07-01-preview"
        openai.api_version = "2023-09-01-preview"

    def wrapper(self, args_dict):
        if type(args_dict) == dict:
            return self.single_turn_wrapper(args_dict)
        elif type(args_dict) == list:
            return self.multi_turn_wrapper(args_dict)

    def single_turn_wrapper(self, args_dict: dict):
        args_dict["messages"] = [{"role": "user", "content": args_dict["message"]}]
        return self.chat_completion(**args_dict)

    def multi_turn_wrapper(self, args_dicts: list):
        messages = []
        messages_text = ""
        for args_dict in args_dicts:
            messages.append({"role": "user", "content": args_dict["message"]})
            messages_text += args_dict["message"] + "\n"
            args_dict["messages"] = messages

            return_dict = self.chat_completion(**args_dict)
            op = return_dict["output"]

            messages_text += op + "\n"
            messages.append({"role": "assistant", "content": op})

        return_dict["message"] = messages_text
        return return_dict

    def chat_completion_mp(self, lst, threads=2):
        if not self.loaded:
            self.load()
            self.loaded = True
        with multiprocessing.Pool(threads) as pool:
            results = list(tqdm(pool.imap(self.wrapper, lst), total=len(lst)))
        return results

    def chat_completion(self, **kwargs):
        if not self.loaded:
            self.load()
            self.loaded = True
        total_try_count = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    engine=self.engine,
                    model=self.model,
                    messages=kwargs["messages"],
                    temperature=self.temperature,  # this is the degree of randomness of the model's output
                )
                return dict(output=response.choices[0].message["content"], **kwargs)
            except Exception as e:
                print(f"OPENAI timeout: {e}")
            time.sleep(5)
            total_try_count += 1
            if total_try_count > 10:
                return "Exceed maximum number of attempts"

    def generate(self, input):
        if not self.loaded:
            self.load()
            self.loaded = True
        total_try_count = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    engine=self.engine,
                    model=self.model,
                    messages=[{"role": "user", "content": input}],
                    temperature=self.temperature,  # this is the degree of randomness of the model's output
                )
                return response.choices[0].message["content"]
            except Exception as e:
                print(f"OPENAI timeout: {e}")
            time.sleep(5)
            total_try_count += 1
            if total_try_count > 10:
                return "Exceed maximum number of attempts"


class Gemini(BaseModel, arbitrary_types_allowed=True):
    loaded: bool = False
    temperature: Optional[float] = 0.0
    model_name: Optional[str]
    model: Optional[genai.GenerativeModel]
    config: Optional[genai.GenerationConfig]

    def load(self):
        genai.configure(api_key=os.environ["GEMINIAPI"])
        self.model = genai.GenerativeModel(self.model_name)
        if self.temperature:
            self.config = genai.GenerationConfig(temperature=self.temperature)
        else:
            self.config = genai.GenerationConfig(
                temperature=self.temperature, top_p=1, top_k=1
            )

    def generate(self, input):
        if not self.loaded:
            self.load()
            self.loaded = True
        while True:
            try:
                response = self.model.generate_content(
                    input, generation_config=self.config
                ).text
                return response
            except Exception:
                response = self.model.generate_content(input).text
                print("error", response)
            time.sleep(5)


def select_model(model_name, **kwargs):
    if model_name == "vicuna":
        path = "lmsys/vicuna-13b-v1.5"
        model = VLLM(model_path=path, **kwargs)
    elif model_name == "platypus2":
        path = "TheBloke/Platypus2-70B-AWQ"
        model = VLLM(model_path=path, **kwargs)
    elif model_name == "flan":
        path = "google/flan-t5-xxl"
        model = SeqToSeqModel(model_path=path, **kwargs)
    elif model_name == "llama2":
        path = "TheBloke/Llama-2-70B-chat-AWQ"  # "meta-llama/Llama-2-70b-chat-hf",
        model = VLLM(model_path=path, **kwargs)
    elif model_name == "llama3":
        model = Llama3(**kwargs)
    elif model_name == "codellama":
        path = "TheBloke/CodeLlama-70B-Instruct-AWQ"
        model = VLLM(model_path=path, **kwargs)
    elif model_name == "gpt4":
        model = GPT4(version="4")
    elif model_name == "chatgpt":
        model = GPT4(version="chat")
    elif model_name == "orca2":
        path = "Open-Orca/Mistral-7B-OpenOrca"
        model = VLLM(model_path=path, **kwargs)
    elif model_name == "metamath":
        # path = "meta-math/MetaMath-7B-V1.0"
        # model = CausalModel(model_path=path, **kwargs)
        path = "TheBloke/MetaMath-70B-V1.0-AWQ"
        model = VLLM(model_path=path, temperature=0.7, top_p=0.95, top_k=40, **kwargs)
    elif model_name == "gemini-pro":
        model = Gemini(model_name="gemini-pro", **kwargs)
    elif model_name == "gemini-1.5":
        model = Gemini(model_name="gemini-1.5-flash", **kwargs)
    elif model_name == "gemini-1.5-pro":
        model = Gemini(model_name="gemini-1.5-pro", **kwargs)
    else:
        breakpoint()

    return model


def test_model(
    model_name: str = "flan",
    prompt: str = "San Franciso is a",
    **kwargs,
):
    model = select_model(model_name, **kwargs)
    print(locals())
    print(prompt)
    print(model.generate(prompt))


if __name__ == "__main__":
    Fire(test_model)
