import random

from pydantic import BaseModel


class GSM8K_Item(BaseModel):
    context: str
    question: str
    chain_of_thought: str = ""
    answer: str = ""

    def to_string(self):
        if self.context == "nan":
            ret = f"{self.question}"
        elif self.question == "nan":
            ret = f"{self.context}"
        else:
            ret = f"{self.context}\n{self.question}"
        ret = (
            ret.replace("#Rewritten Context#:", "")
            .replace("#Rewritten Question#:", "")
            .replace("#Rewritten Context#", "")
            .replace("#Rewritten Question#", "")
        )
        return ret


class Human_eval_Item(BaseModel):
    function_header: str
    docstring: str
    examples: str
    answer: str = ""
    test_case: str = ""
    entry: str = ""

    def to_string(self):
        if self.function_header == "nan":
            self.function_header = ""
        if self.docstring == "nan":
            self.docstring = ""
        if self.examples == "nan":
            self.examples = ""
        ret = f"{self.function_header}{self.docstring}{self.examples}"
        return ret


class Ontology(BaseModel):
    def gsm8k(self):
        return {
            "Original": ["Original", "Original", "Original", "Original"],
            "Remove Constraint": [
                "Remove Constraint",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Median Inquiry": [
                "Partial Solution",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Solution Plan": [
                "Solution Plan",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Detail Elaboration": [
                "Detail Expansion",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Restrict Question": [
                "Add Restriction",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Further Question": [
                "Subsequent Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Parallel Question": [
                "Concurrent Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Change Query": [
                "Change Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Info Recombination": [
                "Info Recombination",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Theoretical Challenge": [
                "Domain Knowledge",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Value Probability": [
                "Complex Reality",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Code Implementation": [
                "General Solution",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Value Big": [
                "Computation Demand",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Change Subject": [
                "Change Value",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Change Calculation": [
                "Change Operation",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Response": [
                "Symbolic Response",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Relation": [
                "Value Relationship",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Scaling": [
                "Variable Group",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Adaptation": [
                "Backward Reasoning",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "WhatIf Question": [
                "What If",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Solve X": [
                "Solve Value",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Range": [
                "Identify Range",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Identify Assumption": [
                "Inherent Premise",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Info Sufficiency": [
                "Complete Missing",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Question Formulation": [
                "Question Formulation",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Introduce Distraction": [
                "Add Misinformation",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Info Necessity": [
                "Optimize Solution",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Step Necessity": [
                "Step Functionality",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Theoretical Basis": [
                "Theoretical Basis",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Solution Efficiency": [
                "Cost Analysis",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Introduce Ambiguity": [
                "Seek Clarification",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Discuss Separately": [
                "Conditional Analysis",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Introduce Contradiction": [
                "Conflicting Information",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Value Uncommon": [
                "Surface Error",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Value Error": [
                "Hidden Error",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Change Setting": [
                "Setting Rephrase",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Change Sequence": [
                "Change Sequence",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "True False": [
                "Close Format",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Value Structuring": [
                "Data Restructuring",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Identical Question": [
                "Identical Problem",
                "Pairwise Comparison",
                "Format Change",
                "Representational Perturbation",
            ],
            "Binary Coded": [
                "Reasoning Format",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "X Language": [
                "Reasoning Style",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "Alternative Answer": [
                "Alternative Answer",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "Define Rules": [
                "New Rule",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            # "Value Unit": ["NA", "NA", "NA", "NA"],
            # "Value Complex": ["NA", "NA", "NA", "NA"],
            # "Value Type": ["NA", "NA", "NA", "NA"],
            # "Value Negative": ["NA", "NA", "NA", "NA"],
        }

    def human_eval(self):
        return {
            "Original": ["Original", "Original", "Original", "Original"],
            "Remove Constraint": [
                "Remove Constraint",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Helper Function": [
                "Partial Solution",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Solution Plan": [
                "Solution Plan",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Example Detail": [
                "Detail Expansion",
                "Question Simplification",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Restrict Requirement": [
                "Add Restriction",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Further Requirement": [
                "Subsequent Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Parallel Requirement": [
                "Concurrent Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Change Docstring": [
                "Change Question",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Info Recombination": [
                "Info Recombination",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Code Import": [
                "Domain Knowledge",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Example Boundary": [
                "Complex Reality",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Higher Order": [
                "General Solution",
                "Reasoning Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Generalize Parameter": [
                "Computation Demand",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Parameter Content": [
                "Change Value",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Type": [
                "Change Operation",
                "Computation Adjustment",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Code Execution": [
                "Symbolic Response",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Parameter Relationship": [
                "Value Relationship",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Substitution": [
                "Variable Group",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Reverse Engineering": [
                "Backward Reasoning",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "WhatIf Code": [
                "What If",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Solve Input": [
                "Solve Value",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Variable Range": [
                "Identify Range",
                "Symbolic Manipulation",
                "Logic Alteration",
                "Structural Perturbation",
            ],
            "Test Case": [
                "Inherent Premise",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Incomplete Answer": [
                "Complete Missing",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Question Formulation": [
                "Question Formulation",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Introduce Bias": [
                "Add Misinformation",
                "Question Understanding",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Reduce Complexity": [
                "Optimize Solution",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Step Necessity": [
                "Step Functionality",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Theoretical Basis": [
                "Theoretical Basis",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Code Complexity": [
                "Cost Analysis",
                "Solution Evaluation",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Example Requirement": [
                "Seek Clarification",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Incomplete Requirement": [
                "Conditional Analysis",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Wrong Example": [
                "Conflicting Information",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Runtime Error": [
                "Surface Error",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Logical Error": [
                "Hidden Error",
                "Error Debugging",
                "Concept Analysis",
                "Structural Perturbation",
            ],
            "Realworld Usecase": [
                "Setting Rephrase",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Parameter Sequence": [
                "Change Sequence",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "True False": [
                "Close Format",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Complex Docstring": [
                "Data Restructuring",
                "Alternative Format",
                "Format Change",
                "Representational Perturbation",
            ],
            "Identical Code": [
                "Identical Solution",
                "Pairwise Comparison",
                "Format Change",
                "Representational Perturbation",
            ],
            "No Keyword": [
                "Reasoning Format",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "X Language": [
                "Reasoning Style",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "Alternative Answer": [
                "Alternative Answer",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
            "Simple Name": [
                "New Rule",
                "Answer Constraint",
                "Format Constraint",
                "Representational Perturbation",
            ],
        }

    def logic_alteration_category(self, dataset):
        if dataset == "gsm8k":
            return [
                key for key, value in self.gsm8k() if value[2] == "Logic Alteration"
            ]
        elif dataset == "human_eval":
            return [
                key
                for key, value in self.human_eval()
                if value[2] == "Logic Alteration"
            ]


class Dataset(BaseModel):
    def gsm8k_original(self):
        return [
            GSM8K_Item(
                context="John has 3 boxes. Each box is 5 inches by 6 inches by 4 inches. The walls are 1 inch thick.",
                question="What is the total inner volume of all 3 boxes?",
                chain_of_thought="""The walls subtract 2*1=<<2*1=2>>2 inches from each dimension
    So each box has 5-2=<<5-2=3>>3 inch width
    It also has a 6-2=<<6-2=4>>4 inch height
    Finally, it has a 4-2=<<4-2=2>>2 inch depth
    So the inner volume of one box is 4*3*2=<<4*3*2=24>>24 cubic inches
    So in total the inner volume of the 3 boxes is 3*24=<<3*24=72>>72 cubic inches
    """,
                answer="72",
            ),
            GSM8K_Item(
                context="A merchant wants to make a choice of purchase between 2 purchase plans: jewelry worth $5,000 or electronic gadgets worth $8,000. His financial advisor speculates that the jewelry market will go up 2.5% while the electronic gadgets market will rise 1.2% within the same month. If the merchant is looking to maximize profit at the end of this month by making a choice,",
                question="how much profit would this be?",
                chain_of_thought="""If he purchases jewelry, he will make a profit of 2.5% which is $5000*(2.5/100) = $<<5000*(2.5/100)=125>>125
    If he purchases electronic gadgets, he will make a profit of 1.2% which is $8000*(1.2/100) = $<<8000*(1.2/100)=96>>96
    If he wants to maximize profit, since $125 > $96, he will choose to purchase jewelry, thereby making a profit of $<<125=125>>125
    """,
                answer="125",
            ),
            GSM8K_Item(
                context="Kylar went to the store to buy glasses for his new apartment. One glass costs $5, but every second glass costs only 60% of the price. Kylar wants to buy 16 glasses. ",
                question="How much does he need to pay for them?",
                chain_of_thought="""The discount price of one glass is 60/100 * 5 = $<<60/100*5=3>>3.
        If every second glass is cheaper, that means Kylar is going to buy 16 / 2 = <<16/2=8>>8 cheaper glasses.
        So for the cheaper glasses, Kylar is going to pay 8 * 3 = $<<8*3=24>>24.
        And for the regular-priced glasses, Kylar will pay 8 * 5 = $<<8*5=40>>40.
        So in total Kylar needs to pay 24 + 40 = $<<24+40=64>>64 for the glasses he wants to buy.
        """,
                answer="64",
            ),
            GSM8K_Item(
                context="Vicki is planning a pop concert at her high school. The show will be 2 hours. She is allowing each group 2 minutes to get on stage, 6 minutes to perform, and then 2 minutes to exit the stage. If she allows a 10-minute intermission,",
                question="how many groups can perform in the concert?",
                chain_of_thought="""First, we should convert the 2 hours of showtime into minutes for our calculations. Since there are 60 minutes in 1 hour, the show will be 2 x 60 = <<2*60=120>>120 minutes. Of those 120 minutes, 10 will be used for intermission, so 120 – 10 = <<120-10=110>>110 minutes for performances. Each group will use 2 minutes to get on stage + 6 minutes to perform + 2 minutes to exit the stage = <<2+6+2=10>>10 minutes of show time. Of the 110 minutes of performances, 10 are used per group, so 110 minutes / 10 = <<110/10=11>>11 groups can perform.""",
                answer="11",
            ),
            GSM8K_Item(
                context="Together Lily, David, and Bodhi collected 43 insects. Lily found 7 more than David. David found half of what Bodhi found. ",
                question="How many insects did Lily find?",
                chain_of_thought="""Let B = the number of insects Bodhi collected
David = B/2
Lily = B/2 + 7
B + B + 7 = 43
2B = <<36=36>>36
B = <<18=18>>18 insects
David = 18/2 = <<18/2=9>>9 insects
Lily = 9 + 7 = <<9+7=16>>16 insects
Lily found <<16=16>>16 insects.""",
                answer="16",
            ),
        ]

    def human_eval_original(self):
        return [
            Human_eval_Item(
                function_header="""
def is_nested(string):
""",
                docstring='''
"""
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.
"""
''',
                examples='''
"""
    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
"""
''',
                test_case="""
def check(candidate):

    # Check some simple cases
    assert candidate('[[]]') == True, ""This prints if this assert fails 1 (good for debugging!)""
    assert candidate('[]]]]]]][[[[[]') == False
    assert candidate('[][]') == False
    assert candidate(('[]')) == False
    assert candidate('[[[[]]]]') == True
    assert candidate('[]]]]]]]]]]') == False
    assert candidate('[][][[]]') == True
    assert candidate('[[]') == False
    assert candidate('[]]') == False
    assert candidate('[[]][[') == True
    assert candidate('[[][]]') == True

    # Check some edge cases that are easy to work out by hand.
    assert candidate('') == False, ""This prints if this assert fails 2 (also good for debugging!)""
    assert candidate('[[[[[[[[') == False
    assert candidate(']]]]]]]]') == False

""",
                answer="""
    opening_bracket_index = []
    closing_bracket_index = []
    for i in range(len(string)):
        if string[i] == '[':
            opening_bracket_index.append(i)
        else:
            closing_bracket_index.append(i)
    closing_bracket_index.reverse()
    cnt = 0
    i = 0
    l = len(closing_bracket_index)
    for idx in opening_bracket_index:
        if i < l and idx < closing_bracket_index[i]:
            cnt += 1
            i += 1
    return cnt >= 2
""",
                entry="is_nested",
            )
        ]
        return [
            Human_eval_Item(
                function_header="""
def flip_case(string: str) -> str:
""",
                docstring='''
    """For a given string, flip lowercase characters to uppercase and uppercase to lowercase."""
''',
                examples='''
    """>>> flip_case('Hello')
    'hELLO'
    """
''',
                answer="""


    return string.swapcase()
""",
                test_case="""
METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate('') == ''
    assert candidate('Hello!') == 'hELLO!'
    assert candidate('These violent delights have violent ends') == 'tHESE VIOLENT DELIGHTS HAVE VIOLENT ENDS'
""",
                entry="flip_case",
            ),
            Human_eval_Item(
                function_header="""
def derivative(xs: list):
""",
                docstring='''
    """ xs represent coefficients of a polynomial.
    xs[0] + xs[1] * x + xs[2] * x^2 + ....
    Return derivative of this polynomial in the same form.
    """
''',
                examples='''
    """
    >>> derivative([3, 1, 2, 4, 5])
    [1, 4, 12, 20]
    >>> derivative([1, 2, 3])
    [2, 6]
    """
''',
                answer="""


    return [(i * x) for i, x in enumerate(xs)][1:]
""",
                test_case="""
METADATA = {}


def check(candidate):
    assert candidate([3, 1, 2, 4, 5]) == [1, 4, 12, 20]
    assert candidate([1, 2, 3]) == [2, 6]
    assert candidate([3, 2, 1]) == [2, 2]
    assert candidate([3, 2, 1, 0, 4]) == [2, 2, 0, 16]
    assert candidate([1]) == []
""",
                entry="derivative",
            ),
            Human_eval_Item(
                function_header="""
def greatest_common_divisor(a: int, b: int) -> int:
""",
                docstring='''
    """ Return a greatest common divisor of two integers a and b
    """
''',
                examples='''
    """
    >>> greatest_common_divisor(3, 5)
    1
    >>> greatest_common_divisor(25, 15)
    5
    """
    ''',
                answer="""


    while b:
        a, b = b, a % b
    return a
""",
                test_case="""
METADATA = {
    'author': 'jt',
    'dataset': 'test'
}


def check(candidate):
    assert candidate(3, 7) == 1
    assert candidate(10, 15) == 5
    assert candidate(49, 14) == 7
    assert candidate(144, 60) == 12
""",
                entry="greatest_common_divisor",
            ),
            Human_eval_Item(
                function_header="""
def is_nested(string):
""",
                docstring='''
"""
    Create a function that takes a string as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.
"""
''',
                examples='''
"""
    is_nested('[[]]') ➞ True
    is_nested('[]]]]]]][[[[[]') ➞ False
    is_nested('[][]') ➞ False
    is_nested('[]') ➞ False
    is_nested('[[][]]') ➞ True
    is_nested('[[]][[') ➞ True
"""
''',
                test_case="""
def check(candidate):

    # Check some simple cases
    assert candidate('[[]]') == True, ""This prints if this assert fails 1 (good for debugging!)""
    assert candidate('[]]]]]]][[[[[]') == False
    assert candidate('[][]') == False
    assert candidate(('[]')) == False
    assert candidate('[[[[]]]]') == True
    assert candidate('[]]]]]]]]]]') == False
    assert candidate('[][][[]]') == True
    assert candidate('[[]') == False
    assert candidate('[]]') == False
    assert candidate('[[]][[') == True
    assert candidate('[[][]]') == True

    # Check some edge cases that are easy to work out by hand.
    assert candidate('') == False, ""This prints if this assert fails 2 (also good for debugging!)""
    assert candidate('[[[[[[[[') == False
    assert candidate(']]]]]]]]') == False

""",
                answer="""
    opening_bracket_index = []
    closing_bracket_index = []
    for i in range(len(string)):
        if string[i] == '[':
            opening_bracket_index.append(i)
        else:
            closing_bracket_index.append(i)
    closing_bracket_index.reverse()
    cnt = 0
    i = 0
    l = len(closing_bracket_index)
    for idx in opening_bracket_index:
        if i < l and idx < closing_bracket_index[i]:
            cnt += 1
            i += 1
    return cnt >= 2
""",
                entry="is_nested",
            ),
            Human_eval_Item(
                function_header="""
def sum_squares(lst):
""",
                docstring='''
    """"
    This function will take a list of integers. For all entries in the list, the function shall square the integer entry if its index is a 
    multiple of 3 and will cube the integer entry if its index is a multiple of 4 and not a multiple of 3. The function will not 
    change the entries in the list whose indexes are not a multiple of 3 or 4. The function shall then return the sum of all entries. 
    """
    ''',
                examples='''
    """
    Examples:
    For lst = [1,2,3] the output should be 6
    For lst = []  the output should be 0
    For lst = [-1,-5,2,-1,-5]  the output should be -126
    """
    ''',
                answer="""
    result =[]
    for i in range(len(lst)):
        if i %3 == 0:
            result.append(lst[i]**2)
        elif i % 4 == 0 and i%3 != 0:
            result.append(lst[i]**3)
        else:
            result.append(lst[i])
    return sum(result)
""",
                test_case="""
def check(candidate):

    # Check some simple cases

    assert candidate([1,2,3]) == 6
    assert candidate([1,4,9]) == 14
    assert candidate([]) == 0
    assert candidate([1,1,1,1,1,1,1,1,1]) == 9
    assert candidate([-1,-1,-1,-1,-1,-1,-1,-1,-1]) == -3
    assert candidate([0]) == 0
    assert candidate([-1,-5,2,-1,-5]) == -126
    assert candidate([-56,-99,1,0,-2]) == 3030
    assert candidate([-1,0,0,0,0,0,0,0,-1]) == 0
    assert candidate([-16, -9, -2, 36, 36, 26, -20, 25, -40, 20, -4, 12, -26, 35, 37]) == -14196
    assert candidate([-1, -3, 17, -1, -15, 13, -1, 14, -14, -12, -5, 14, -14, 6, 13, 11, 16, 16, 4, 10]) == -1448


    # Don't remove this line:
""",
                entry="sum_squares",
            ),
        ]


class PromptTemplate(BaseModel):
    def check_gsm8k_prompt(self, question, generated_answer, gold_answer):
        return f"""Below is a #question#, Check if the #generated answer# is correct by comparing it with the #gold answer#. You only need to compare the final answer. If the expression in #generated answer# and #gold answer# are equivalent mathematically, it is also considered as correct. If correct, output True, otherwise output False.
#question#:
{question}

#gold answer#:
{gold_answer}

#generated answer#:
{generated_answer}
"""

    def testcase_input_prompt(self, perturbed_question, reference):
        return f"""Create input parameters for test cases that align with the following #coding requirement#. Focus solely on the input values for these test cases. The input parameters should encompass boundary conditions within the scope defined by the function's requirements specification, and avoid scenarios that fall outside of these requirements. You should generate three to eight test cases.
test_case1: [input parameters 1]
test_case2: [input parameters 2]

#coding requirement#: 
{perturbed_question}
#You can also choose from some references from below#:
{reference}
"""

    def testcase_output_prompt(self, answer, test_input):
        local_scope = {}
        answer = "from typing import *\n" + answer
        exec(answer, local_scope)

        parsed_cases = dict()
        test_input = test_input.encode("ascii", "ignore").decode()
        for line in test_input.strip().split("\n"):
            case_name, case_value = line.split(":", 1)
            try:
                test_case = eval(case_value.strip())
                parsed_cases[case_name] = test_case
            except Exception:
                pass

        output_string = ""
        for case_name, test_input in parsed_cases.items():
            try:
                output = local_scope["gold_solution"](*test_input)
                if isinstance(output, str):
                    output_string += f"{case_name}: '{output}'\n"
                else:
                    output_string += f"{case_name}: {output}\n"
            except Exception:
                pass
        return output_string

    def testcode_prompt(self, perturbed_question, test_input, test_output, generation):
        return f"""#Instruction for Python Code Assertion Generation:
Objective: Create assertion statements in Python to automatically test the extracted code from the provided #answer# using the given #testcase input# against the expected #testcase output#.
Steps:
1. Extract Python Code: Given #coding requirement#, Identify and extract the Python code within the #answer# section.
2. Formulate Assertion Statement: Construct an assertion statement in Python using the extracted code, the provided #testcase input#, and the expected #testcase output#. (If the there is no test_output for test_input, you should ignore that testcase.
Output Format: Your final output should be a Python code snippet formatted as follows:
```python
[extracted python functions]
assert [extracted python functions]([test case input1]) == [test case output1], "testcase 1"
assert [extracted python functions]([test case input2]) == [test case output2], "testcase 2"
...
```

#coding requirement#: {perturbed_question}

#answer#: {generation}

#testcase input#: {test_input}

#testcase output#: {test_output}
"""

    def gsm8k_with_answer_prompt(
        self, perturbed_question, original_question, original_answer
    ):
        prompt = f"""Given the original question and its answer, Solve the question that is a perturbed variant of the original question. Solve the #perturbed question# step by step before give the final answer. Do not directly give the final answer. \n
#Original Question#: {original_question}
#Original Answer#: {original_answer}
#Perturbed Question#: {perturbed_question}
"""
        return prompt

    def gsm8k_consistency_prompt(
        self, oneshot_question, oneshot_answer, perturbed_question
    ):
        prompt = f"""Given the oneshot demonstration of a question and its final answer, Solve the #question# step by step before give the final answer. Do not directly give the final answer. \n
#Demonstration Question#: {oneshot_question}
#Demonstration Final Answer#: {oneshot_answer}

#Question#: {perturbed_question}
Reasoning Step: [Reasoning Steps]
Final answer: [Final answer]
"""
        return prompt

    def gsm8k_summarize_consistency_prompt(
        self, perturbed_question, answer0, answer1, answer2
    ):
        prompt = f"""Instruction: Answer the following question by considering various reasoning pathways shown below and marginalize out reasoning paths to aggregate and get the final answer
Question: {perturbed_question}

Reasoning Pathway 1: {answer0}
Reasoning Pathway 2: {answer1}
Reasoning Pathway 3: {answer2}
"""
        return prompt

    def gsm8k_pot_prompt(self, perturbed_question):
        prompt = f"""Instruction: You are an experienced professional skilled in using python programs to solve math related problems. Solve the question below using python programs, You will only write code blocks.

Problem: {perturbed_question}
"""
        return prompt

    def human_eval_with_answer_prompt(
        self, instruction, perturbed_question, original_function
    ):
        prompt = f"""Given the original python function, solve the problem that requires a perturbed version of the original python function. You should answer the #perturbed problem# in a step by step manner and do not directly give final answer.\n
#Original Function#: {original_function}

#Perturbed Problem#: {instruction}
{perturbed_question}
Solution:
"""
        return prompt

    def gsm8k_cot_prompt(self, perturbed_question, model="default"):
        if model in ["gpt4", "chatgpt", "gemini"]:
            prompt = f"""Solve the question step by step before give the final answer. Do not directly give the final answer.
{perturbed_question}
Reasoning Step: [reasoning steps]
Answer: [final answer]
"""

        else:
            prompt = f"""Below is an instruction that describes a task. Write a response that appropriately completes the request.


### Instruction:
{perturbed_question}


### Response: Let's think step by step.

"""
        return prompt

    def gsm8k_dp_prompt(self, perturbed_question, model="default"):
        if model == "metamath":
            breakpoint()
        else:
            prompt = f"""Solve the question below directly. Please output the final answer in this format: Final Answer: [final answer]
{perturbed_question}
Final Answer:
"""
        return prompt

    def human_eval_cot_prompt(self, instruction, perturbed_question, model="default"):
        if model in ["gpt4", "chatgpt", "gemini"]:
            prompt = f"""Instruction:{instruction}. You should answer the question in a step by step manner and do not directly give final answer.\n
{perturbed_question}
Solution:
"""
        elif model == "llama2":
            prompt = f"""Instruction:{instruction}.
{perturbed_question}
let's answer the question step by step.:
"""
        elif model == "codellama":
            prompt = f"""Source: system

  You should answer the question follow the instruction in a step by step manner and do not directly give final answer. <step> Source: user

  Instruction: {instruction}\n{perturbed_question}  <step> Source: assistant
   
"""
        return prompt

    def human_eval_dp_prompt(self, instruction, perturbed_question):
        prompt = (
            f"""Instruction:{instruction}. You should give the final answer directly without thinking step by step.\n
{perturbed_question}
Answer: [final answer]
""",
        )
        return prompt


class PerturbTemplate(BaseModel):
    def gsm8k(self, item, dimension, model):
        if dimension == "Restrict Question":
            prompt = "Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += "#Rewrite Requirement#:1. Add a new info to context or a constraint on the original question. 2. the answer to the rewritten question should be harder than the original answer.\n"
            prompt += f"#Original Question#:{item.context}{item.question}\n"
            prompt += "#Rewritten Question#:\n"
            item.context = ""
            item.question = model(prompt)
            item.answer = ""

        elif dimension == "Further Question":
            prompt = "Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "Your output should be: [#Further Question#]\n"
            prompt += "#Rewrite Requirement#:1. No change to the original context. 2. keep the original question 3. add a question that requires further calculation by utilizing the answer of original question, the added question should be harder and solvable\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Further Question#:\n"
            item.question = item.question + " " + model(prompt)
            item.answer = ""

        elif dimension == "Parallel Question":
            prompt = "Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"
            prompt = "Your output should only be: [#Parallel Question#]\n"
            prompt += "#Rewrite Requirement#:1. No change to the original context. 2. keep the original question 3. add an additional question that ask for values independent from the answer of original question from the same context. The added question should be harder and solvable\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Parallel Question#:\n"
            item.question = item.question + " " + model(prompt)
            item.answer = ""

        elif dimension == "Remove Constraint":
            to_change = "Context"
            prompt = f"""Instruction: Rewrite below original mathematical {to_change} based on the #rewrite requirement#.\nYour output should only be: [#Rewritten {to_change}#]\n"""
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewrite Requirement#:1. Remove some constraint or information from the original context. 2. make sure the rewritten question can still be solved, but answer is simpler. \n"
            prompt += f"#Rewritten {to_change}#:\n"
            item.context = model(prompt)
            item.answer = ""

        elif dimension == "Median Inquiry":
            to_change = "Question"
            prompt = f"""Instruction: Rewrite below original mathematical {to_change} based on the #rewrite requirement#.\n Your output should be: [#Rewritten {to_change}#]\n"""
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += (
                f"#Step by Step Answer to Original Question#: {item.chain_of_thought}\n"
            )
            prompt += "#Rewrite Requirement#:1. No change to the original context. 2. Change the question to ask one of any intermediate results from the step by step answer to the original question\n"
            prompt += f"#Rewritten {to_change}#:\n"
            item.question = model(prompt)
            item.answer = ""

        elif dimension == "Change Query":
            to_change = "Question"
            prompt = f"""Instruction: Rewrite below original mathematical {to_change} based on the #rewrite requirement#.\n Your output should be: [#Rewritten {to_change}#]\n"""
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewrite Requirement#:1. do not change the context of original question 2. Change the question to ask for another value that is different from the value asked in original question\n"
            prompt += f"#Rewritten {to_change}#:\n"
            item.question = model(prompt)
            item.answer = ""

        elif dimension == "Change Setting":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += """#rewrite requirement#: Rephrase the original question by changing the application scenario or situation to a completely different one but keep the math core structure. Then change all the person's names and values\n Your output should be: [#Rewritten Question#]\n"""
            prompt += f"#Original Question#:{item.context} Query: {item.question}\n"
            prompt += "[#Rewritten Question#]\n"
            item.context = ""
            item.question = model(prompt)
            item.answer = ""

        elif dimension == "Change Calculation":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#Rewritten requirement#: Change one information in original context, so that it changes the math calculation operation(+-*/) when answering the question based on the context. Make sure the change fits into the context\n"
            prompt += "Your output should only be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewritten Context#:\n"
            item.context = model(prompt)
            item.answer = ""

        elif dimension == "Change Subject":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#Rewritten requirement#: Exchange the Peoples' names among the original context. So one person's name in the original context is change to another person's name. If there is only one person's name in the original context, swap the values\n"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""

        elif dimension == "Info Recombination":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#Rewritten Requirement#: Adapt and merge the mathematical principles from two questions into one coerce question. You do not need to include all the math principles from both questions in the merged question. The final question should ask for only one value. Make sure the Rewritten Question looks natural.\n"
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += f"#Original Question#:{item.context} {item.question}\n"
            prompt += "#Another Question#: James decides to run 3 sprints 3 times a week.  He runs 60 meters each sprint.  How many total meters does he run a week?"
            prompt += "#Rewritten Question#:\n"
            item.context = ""
            item.question = model(prompt)
            item.answer = ""

        elif dimension == "Variable Response":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#Rewritten Requirement#: randomly replace only one value inside original context to variable X\n"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            item.context = model(prompt)
            item.question = (
                item.question
                + "(the answer to the question may have variable X included)"
            )
            item.answer = ""

        elif dimension == "Variable Relationship":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#rewritten requirement#: Find only two values that have a relationship with each other in the original context, and replace the these two values inside the original context to variables X and Y."
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            item.context = model(prompt)
            item.question = (
                item.question
                + f" If the answer to the question is {item.answer}. What is the equation connects the relationship between X and Y?"
            )
            item.answer = ""

        elif dimension == "Variable Scaling":
            prompt = """Instruction: Pick at least 2 values in the context, and output their names separated by comma\n"""
            prompt += f"#Context#:{item.context}\n"
            prompt += "#Variable Names#:\n"
            output = model(prompt)
            item.question = (
                f"If the following values [{output}] is scaled up by variable x. "
                + item.question
                + "(answer may variable x included)\n"
            )
            item.answer = ""

        elif dimension == "Variable Adaptation":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#rewritten requirement#: First pick only one specific value from the original context, and change the rewritten question to the following: If the answer to the original question changes(-/+) by a certain variable X, and how should [the variable you just picked] adjust correspondingly if other values stay the same? "
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewritten Question#:\n"
            item.question = model(prompt) + "(The adjustment may include variable X)"
            item.answer = ""

        elif dimension == "WhatIf Question":
            prompt = """Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"""
            prompt += "#rewrite requirement#: 1. rewrite the original context by removing only one value (the whole sentence contains that value) from the original context and the rewritten context should be understandable by human 2. Pick another specific value from the original context 3. output the following question as [#counterfactual question#]: [your rewritten context here], [place original question here], If we know the answer to the question is [original answer here] and [the name of the value you picked] in the original question is doubled, how would the final answer change?"
            prompt += "Your output should be:\n[#counterfactual question#]\n "
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += f"#Original Answer#:{item.answer}\n"
            prompt += "#Counterfactual Question#:\n"
            output = model(prompt)
            item.context = ""
            item.question = output
            item.answer = ""

        elif dimension == "Theoretical Basis":
            item.question = (
                item.question
                + "\n"
                + "Instruction: You do not need to solve the question, you only need to identify one underlying mathematical background theory to answer the question."
            )
            item.answer = ""

        elif dimension == "Code Implementation":
            item.question = (
                item.question
                + "\nInstruction: You should develop a python code to solve the question (you do not need to solve the question yourself)\nCode Solution:"
            )
            item.answer = ""

        elif dimension == "Solution Plan":
            prompt = "You should suggest solution plan by summarizing the solution below, but remove the calculations from the plan"
            prompt += "Your output should be: [#Solution Plan#]\n"
            prompt += f"#Solution#:{item.chain_of_thought}\n"
            output = model(prompt)
            item.question = (
                item.question + "\nFollow this plan to solve the question:\n" + output
            )
            item.answer = ""

        elif dimension == "Detail Elaboration":
            prompt = "Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Identify the hidden assumptions to answer original question, and rewrite the original context by specifying the hidden assumptions inside the original context."
            prompt += "Your output should only be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""

        elif dimension == "Info Sufficiency":
            if random.choice([True, False]):
                prompt = "Instruction: Rewrite below original mathematical question based on the #rewrite requirement#.\n"
                prompt += "#rewrite requirement#: rewrite the original context by removing one piece of information and make it looks less noticeable"
                prompt += "Your output should be: [#Rewritten Context#]\n"
                prompt += f"#Original Context#:{item.context}\n"
                prompt += "#Rewritten Context#:\n"
                output = model(prompt)
                item.context = output
            item.question = (
                item.question
                + "\n"
                + "You do not need to solve the question, just judge whether The information given in the context is enough to answer the question."
            )
            item.answer = ""

        elif dimension == "Info Necessity":
            if random.choice([True, False]):
                prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
                prompt += "#rewrite requirement#: rewrite the original context by adding one piece of redundant information contain a value and make sure it look not noticeable"
                prompt += "Your output should be: [#Rewritten Context#]\n"
                prompt += f"#Original Context#:{item.context}\n"
                prompt += "#Rewritten Context#:\n"
                output = model(prompt)
                item.context = output
                item.answer = "True"
            else:
                item.answer = "False"
            item.question = (
                item.question
                + "\n"
                + "Instruction: You do not need to solve the question, just judge whether there are redundant values given in order to answer the question?"
            )

        elif dimension == "Step Necessity":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: 1. Pick a value from step by step answer to the original question, and rewrite the original question to the following: Whether there are any alternative solutions without calculating [value name you picked]?"
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += f"Step by Step answer to the original question:{item.chain_of_thought}\n"
            prompt += "#Rewritten Question#:\n"
            output = model(prompt)
            item.context = "Question:\n" + item.context.strip()
            item.question = (
                item.question.strip()
                + "\nTo solve the above math question, "
                + output
                + "(You do not need to solve the question)"
            )
            item.answer = ""

        elif dimension == "Variable Range":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Find only one value that have relationship with other values in the original context, replace that value with variable X in original context"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten COntext#:\n"
            output = model(prompt)
            item.context = output
            item.question = (
                item.question
                + "\n"
                + "Instruction: You do not need to solve the question, just find the possible ranges of values of variable X based on the question"
            )

        elif dimension == "Identical Question":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            if random.choice([True, False]):
                prompt += "#rewrite requirement#: First, change the order of the sequence the information is provided. Second, rephrase the original question by changing the application scenario and values used. Then change the question to make it require more steps to reach the final answer."
                item.answer = "True"

            else:
                prompt += "#rewrite requirement#: First, change the order of the sequence the information is provided. Second, rephrase the original question by changing the application scenario and values used"
                item.answer = "False"
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += f"#Original Question#:{item.context} {item.question}\n"
            prompt += "#Rewritten Question#:\n"
            output = model(prompt)
            item.context = (
                f"Question 1: {item.context} {item.question}\nQuestion 2: {output}\n"
            )
            item.question = (
                "Does Question 1 and Question 2 require same amount step to answer?"
            )

        elif dimension == "Identify Assumption":
            item.context = (
                "Instruction: No need to solve question below, just identify one most important hidden assumption in the question that requires the question to be answerable\n"
                + item.context
            )
            item.answer = ""

        elif dimension == "Discuss Separately":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Replace one value with variable in original context. Make sure that the expression of the answer varies with different range of values of this variable"
            prompt += "Your output should only be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""

        elif dimension == "Theoretical Challenge":
            prompt = "Change the #Question# below to ask for a value that will converge after infinite number of calculations, the result should be human understandable and solvable\n"
            prompt += f"#Question#:{item.context} {item.question}\n"
            output = model(prompt)
            item.question = output
            item.context = ""
            item.answer = ""
        elif dimension == "Define Rules":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: formulate a special mathematical calculation operation that does not exist in real world. Also change the original question to include this rule in the question. Make sure the rewritten question is still human understandable.\n"
            prompt += "Your output should be: [#Rewritten Question#]\n"
            prompt += f"#Original Question#:{item.context} {item.question}\n"
            prompt += "#Rewritten Question#:\n"
            output = model(prompt)
            item.question = output
            item.context = ""
            item.answer = ""
        elif dimension == "Binary Coded":
            n = random.choice([2, 3, 4, 5, 6])
            item.context = (
                f"Instruction: Answer the following question with only base-{n} coded values:\n"
                + item.context
            )
            item.answer = ""
        elif dimension == "X Language":
            language = random.choice(
                ["Spanish", "Chinese", "Bengali", "French", "Russian"]
            )
            item.context = (
                f"Instruction: Answer the following question with only {language} language, because I do not understand English\n"
                + item.context
            )
            item.answer = ""
        elif dimension == "Alternative Question":
            item.context = (
                "Instruction: Rephrase the question above in another application scenario without changing the mathematical core structure of the question, you do not need to answer it: \n"
                + item.context
            )
            item.answer = ""
        elif dimension == "Alternative Answer":
            prompt = "Remove all the mathematical calculation, equation and numbers from the solution below, make sure the output is still human understandable:\n"
            prompt += f"#Solution#:{item.chain_of_thought}\n"
            output = model(prompt)
            item.context = (
                "Instruction: Give an alternative step by step solution and calculate the answer to the following question that is different from the solution below.\nQuestion:"
                + item.context
            )
            item.question = (
                item.question
                + "\nSolution:\n"
                + output
                + "\nAlternative Step by Step Solution:"
            )
            item.answer = ""
        elif dimension == "Question Formulation":
            item.context = "Instruction: Formulate a math application question that requires the following calculations\n"
            prompt = f"Instruction: Extract the math calculations only inside the following sentences.\n{item.chain_of_thought}"
            output = model(prompt)
            item.question = "Calculations:\n" + output + "\nMath Question:"
            item.answer = ""

        elif dimension == "Solve X":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: randomly pick a specific value in original context and replace it with variable X"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.question = (
                item.question
                + "\n"
                + f"If the answer for the question is {item.answer} what is the value for X"
            )
            item.answer = ""
        elif dimension == "Change Sequence":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: change the order sequence of the information completely in the original context. Make sure the rewritten context is still human readable"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = item.answer
        elif dimension == "Value Structuring":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: use variables to replace the values in the original context and put the variables' values inside the question to a table format"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = item.answer
        elif dimension == "True False":
            if not random.choice([True, False]):
                prompt = "Instruction: Give one step by step misleading answer for this question that seems corerct:"
                prompt += f"#Original Question#:{item.context} {item.question}\n"
                prompt += "Your output should be: [#Misleading Answer#]\n"
                output = model(prompt)
                item.question = (
                    item.question + f"Evaluate the correctness of this answer: {output}"
                )
                item.answer = "False"
            else:
                item.question = (
                    item.question
                    + f"Evaluate the correctness of this answer: {item.answer}"
                )
                item.answer = "True"
        elif dimension == "Introduce Distraction":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: introduce a few new pieces of information as distraction in the original context that at first glance seems affecting the final answer but in fact should not affect the answer to the question"
            prompt += "Your output should only be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = item.answer

        elif dimension == "Introduce Contradiction":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Introduce a intermediate variable with value conflicting with the chain of thought answer below. The added value should not directly conflict with information inside the question"
            prompt += "Your output should only be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += f"#Original Question#:{item.question}\n"
            prompt += f"#Chain of thought answer to the original question#: {item.chain_of_thought}"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = "no correct answer"
        elif dimension == "Introduce Ambiguity":
            prompt = "Change the original question to have multiple possible interpretations\n"
            prompt += f"#Question#:{item.context}{item.question}\n"
            prompt += "#Rewritten Question#:\n"
            output = model(prompt)
            item.context = ""
            item.question = output
            item.answer = "no correct answer"

        elif dimension == "Value Uncommon":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: use uncommon values in the original context that seems wired or impossible by commonsense"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = "no correct answer"

        elif dimension == "Value Error":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change the values in original context so that it can cause a commonsense error or logical error in the question"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = "no correct answer"
        elif dimension == "Value Big":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change the values in the original context a lot bigger than its original values"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""
        elif dimension == "Value Unit":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change only one values' unit in the original context to a different unit"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""
        elif dimension == "Value Complex":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change one or two values in the original context to a more complex 5 digit value that poses a challenge for computation (You do not need to change all the values)"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""
        elif dimension == "Value Type":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change the values in the original context to a different type of value (e.g. from integer to float or fractions). The values do not need to be the same"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""
        elif dimension == "Value Probability":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change only one deterministic value in the original context to one with probability. For example, The value have a 30% chance to be 10, and 70% chance to be 17. Make sure The rewritten context should be understandable by human"
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.question += "(Give the estimated value)"
            item.answer = ""
        elif dimension == "Value Negative":
            prompt = "Instruction: Rewrite the below original mathematical question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change only one value in the original context to negative value. The values do not need to be the same."
            prompt += "Your output should be: [#Rewritten Context#]\n"
            prompt += f"#Original Context#:{item.context}\n"
            prompt += "#Rewritten Context#:\n"
            output = model(prompt)
            item.context = output
            item.answer = ""
        else:
            print("Error:", dimension)

        return item

    def human_eval(self, item, dimension, model):
        if dimension == "Restrict Requirement":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Add a new further condition that modifies the coding requirement in #original coding question# that make the coding requirment harder\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Further Requirement":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Add a further requirement on top of the achieved results in #original coding question#\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Parallel Requirement":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Add a further requirement that can be achieved in parallel with the requirement in #original coding question#\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Remove Requirement":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Make the requirement in #original coding question# easier.\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Helper Function":
            # Question
            prompt = "#rewrite requirement#: Add a helper function that can help to partially achieve the requirement in #original coding question# You do not need to answer the question\n"
            prompt += "Your output should be python program only: [#Helper Function#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Helper Function#:\n"
            output = model(prompt)
            item.function_header = output + "\n" + item.function_header
            item.docstring = (
                item.docstring
                + '''    """\nUse the helper function above to achieve the requirement"""'''
            )
            item.answer = ""

        elif dimension == "Change Docstring":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Change the requirement in docstring in #original coding question# to require a related but different solution\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Change Example":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Generate new examples in #original coding question examples#, Make sure the generated examples is still correct based on the requirement described in the docstring, keep the number of examples same as before\n"
            prompt += "Your output should only be: [#Rewritten Coding Examples#]\n"
            prompt += f"#Original Coding Question Function Header#:{item.function_header}{item.docstring}\n"
            prompt += "#Original Coding Question Examples#:{item.examples}\n"
            prompt += "#Rewritten Coding Examples#:\n"
            output = model(prompt)
            if not ('"""' in output or "'''" in output):
                output = "'''" + "\n" + output + "\n" + "'''"
            item.examples = output
            item.answer = ""

        elif dimension == "Parameter Content":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Revise the definition and purpose of the input parameter in the function described in the #original coding question#. Additionally, update the function's docstring to accurately reflect the new meaning and role of the parameter.\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Parameter Type":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Keep the same requirement except changing the type of the parameter in #original coding question#. For example, you can change int to str\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Info Recombination":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Merge the two #original coding question# into one super question that contains the elements of both questions. The super question do not need to contain every information provided in the two #original coding question#.\n"
            prompt += "The rewritten coding question should contain the function header, the docstring with examples. Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question 1#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += '''#Original Coding Question 2#:

    def solution(lst):
        """Given a non-empty list of integers, return the sum of all of the odd elements that are in even positions.


        Examples
        solution([5, 8, 7, 1]) ==> 12
        solution([3, 3, 3, 3, 3]) ==> 9
        solution([30, 13, 24, 321]) ==>0
        """
    '''
            prompt += "#Rewritten Coding Question#:\n"

            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Variable Iteration":
            # Question
            prompt = "Instruction: Give only one specific input values that can feed to the program header below"
            prompt += f"program:{item.function_header}{item.docstring}{item.examples}{item.answer}\n"
            output = model(prompt)
            item.function_header = (
                "The below program is fed with: "
                + output
                + " as input and feedback the function output to its input variable, and the function is executed for X number of times, what is the final output? (answer may have variable X included)"
                + "\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""

        elif dimension == "Variable Substitution":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Substitute one specific value in docstring as a input parameter to the function."
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "WhatIf Code":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Make a small change to the function below. This change should slightly alter what the function does, but keep it mostly the same.\n"
            prompt += "Your output should only contain the rewritten python code"
            prompt += (
                f"#Function#:{item.function_header}{item.docstring}{item.answer}\n"
            )
            prompt += "#Rewritten Coding Question#:\n"
            rewritten_code = model(prompt)
            prompt = "Choose one example below and mask only one of the input value with variable in the example with masked_input. Please give me the example after masking\n"
            prompt += f"#Examples#:{item.examples}\n"
            prompt += "#Masked Example#:\n"
            masked_example = model(prompt)

            item.function_header = f"""If the output to the following function is \n{masked_example}\nFunction:\n
    {item.function_header}{item.docstring}{item.answer}
    What if the function is now changed to:
    {rewritten_code}
    What will be the output to the function?
    """
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Generalize Parameter":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Generalize the input parameter class type by expanding to one or more python classes, for example string, dict and list, float. The requirement should also expand accordingly to achieve similar requirements for those expanded types\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Higher Order":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: Identify a broader requirement that encompasses the specific coding problem presented below. \n"
            prompt += "Your output should be: [#Rewritten Coding Requirement#]. You should describe the requirement using natural language. and give some examples to illustrate it\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = (
                "Write a higher order function that can solve the problem: \n"
                + output
                + "\nBelow is a special case that can solve the above problem\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""
        elif dimension == "Code Plan":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: The rewritten question should suggest a commented solution plan add add it at the back of original coding question, without giving implementation specified in the plan.\n"
            prompt += "Your output should be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = item.function_header + "\n" + output
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Code Execution":
            # Question
            prompt = "Instruction: Find only one set of values for the input parameters that can be used for the function below.\n"
            prompt += (
                f"#Function#:{item.function_header}{item.docstring}{item.answer}\n"
            )
            prompt += "#Input Values#:\n"
            input_values = model(prompt)
            item.function_header = (
                f"Find the output of the following function, if the input is:{input_values}\n"
                + item.function_header
            )
            item.examples = ""
            item.answer = ""
        elif dimension == "RealWorld Usecase":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: The rewritten docstring should frame the function requirment in a real world scenario that uses this function. The rewritten function requirement may be different from the original requirement. You should also change the function name\n"
            prompt += "Your output should only be: [#Rewritten Coding Docstring#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "#Rewritten Coding Question#:\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""

        elif dimension == "Compare Efficiency":
            # Question
            prompt = "Instruction: Rewrite the below original coding question based on the #rewrite requirement#.\n"
            prompt += "#rewrite requirement#: write the code below to a more efficient or inefficient version with the same functionality. (choose one)\n"
            prompt += "Your output should only be: [#Rewritten Coding Question#]\n"
            prompt += f"#Original Coding Question#:{item.function_header}{item.docstring}{item.answer}\n"
            output = model(prompt)
            item.function_header = (
                f"Which function below is more efficient:?\nCode 1:\n{output}\nCode 2:\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""

        elif dimension == "Time Complexity":
            # Question
            item.function_header = (
                "Analyze the complexity regarding to each input parameter of the following function:\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""

        elif dimension == "Space Complexity":
            # Question
            item.function_header = (
                "Analyze the space complexity regarding to each input parameter of the following function:\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""
        elif dimension == "Parameter Categorization":
            # Question
            item.function_header = (
                "Categorize the input parameters of the following function into groups, and give a representation of each group\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""
        elif dimension == "Output Categorization":
            # Question
            item.function_header = (
                "Categorize the potential output of the following function into groups\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""
        elif dimension == "Test Case":
            # Question
            item.function_header = (
                "Write test cases that can test for the following function\n"
                + item.function_header
            )
            item.answer = ""

        elif dimension == "Guess Input":
            # Question
            prompt = f"Give only one possible output for the following function\n{item.function_header}{item.docstring}{item.answer}\n"
            prompt += "You should only give output, and should not give input\n"
            prompt += "[#Possible Output#]:\n"
            possible_output = model(prompt)
            item.function_header = (
                "What are possible input to the following function, if the output is:\n"
                + possible_output
                + "\n"
                + item.function_header
            )
            item.examples = item.answer
            item.answer = ""

        elif dimension == "Code Import":
            # Question
            item.function_header = (
                "Rewrite the function below to take in batch input parameter and use the multicore cpu.\n"
                + item.function_header
            )
            item.examples = item.examples + item.answer
            item.answer = ""
        elif dimension == "No ForLoop":
            # Question
            item.function_header = (
                "Instruction: Answer the coding function below without using for loop\n"
                + item.function_header
            )
            item.answer = ""
        elif dimension == "X Language":
            # Question
            language = random.choice(["python2", "c++", "java", "javascript", "go"])
            prompt = f"Rewrite the function header below in {language} (you do not need to answer it)\n"
            prompt += f"{item.function_header}{item.docstring}{item.examples}\n"
            output = model(prompt)
            item.function_header = (
                f"Answer the coding question below in {language}\n" + output
            )
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Simple Name":
            # Question
            item.function_header = (
                "Answer the coding question below and only use 6 letter word for each variable names inside the solution\n"
                + item.function_header
            )
            item.answer = ""
        elif dimension == "Alternative Question":
            # Question
            item.function_header = (
                "Rewrite the function description to a completely different one without changing its functionality\n"
                + item.function_header
            )
            item.answer = ""
        elif dimension == "Alternative Answer":
            # Question
            item.function_header = (
                "Find an alternative solution for the following coding question\n"
                + item.function_header
            )
            item.examples = item.examples + "Solution:\n" + item.answer.strip()
            item.answer = ""
        elif dimension == "Question Formulation":
            # Question
            item.function_header = "Write a code description for the following code and provide one use case\n"

            item.docstring = ""
            item.examples = item.answer
            item.answer = ""
        elif dimension == "Backward Function":
            # Question
            prompt = "Describe a function requirement that reverse engineer the given function, you should also together give docstring and function header\n"
            prompt += (
                f"{item.function_header}{item.docstring}{item.examples}{item.answer}\n"
            )
            new_requirement = model(prompt)
            item.function_header = new_requirement
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Parameter Sequence":
            # Question
            prompt = "Instruction: Change the input parameter sequence of the function header below then Change the input parameter name and function name to wired names of the function header below"
            prompt += f"#Function Header#:{item.function_header}{item.docstring}{item.examples}\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Incomplete Answer":
            # Question
            item.function_header = (
                "Fulfill the coding question below\n" + item.function_header
            )
            item.examples = item.examples + item.answer.strip()[:10]
            item.answer = ""
        elif dimension == "True False":
            # Question
            if random.choice([True, False]):
                item.function_header = (
                    "Evaluate whether the solution below is the correct solution for the coding question, True or False?\nCoding Question:\n"
                    + item.function_header
                )
                item.examples = item.examples + "Solution:\n" + item.answer
                item.answer = "True"
            else:
                prompt = "Generate a wrong and misleading solution for the following coding question\nCoding Question:\n"
                prompt += (
                    item.function_header + item.docstring + item.examples + item.answer
                )
                output = model(prompt)
                item.function_header = (
                    "Evaluate whether the solution below is the correct solution for the coding question, True or False?\nCoding Question:\n"
                    + item.function_header
                )
                item.examples = item.examples + "Solution:\n" + output
                item.answer = "False"
        elif dimension == "One Example":
            # Question
            prompt = (
                "Rewrite the function below to only take one example as demonstration. You do not need to complete the function.\n"
                + item.function_header
                + item.docstring
                + item.examples
            )
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = item.answer
        elif dimension == "Wrong Example":
            # Question
            prompt = (
                "Rewrite the function below to use a misleading example as demonstration\n"
                + item.function_header
                + item.docstring
                + item.examples
            )
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = "no correct answer"
        elif dimension == "Syntax Error":
            prompt = "Introduce a Syntax Error to the following function that is hard to notice and debug. You should not add any new lines of code\n"
            prompt += f"#Function Header#:{item.function_header}{item.docstring}{item.examples}{item.answer}\n"
            wrong_code = model(prompt)
            item.function_header = (
                "Debug the error in the following code\n" + wrong_code
            )
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Logical Error":
            prompt = "Introduce a Logical Error to the following function that is hard to notice and debug. You should not add any new lines of code\n"
            prompt += f"#Function Header#:{item.function_header}{item.docstring}{item.examples}{item.answer}\n"
            wrong_code = model(prompt)
            item.function_header = (
                "Debug the error in the following code\n" + wrong_code
            )
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Runtime Error":
            prompt = "Introduce a Runtime Error to the following function that is hard to notice and debug. You should not add any new lines of code\n"
            prompt += f"#Function Header#:{item.function_header}{item.docstring}{item.examples}{item.answer}\n"
            wrong_code = model(prompt)
            item.function_header = (
                "Debug the error in the following code\n" + wrong_code
            )
            item.docstring = ""
            item.examples = ""
            item.answer = ""
        elif dimension == "Example Count":
            prompt = "Add ten more correct demonstrations examples in the function docstring:\n"
            prompt += f"{item.function_header}{item.docstring}{item.examples}\n"
            prompt += "You should only output examples"
            output = model(prompt)
            item.examples = output
            item.answer = item.answer
        elif dimension == "Example Complex":
            prompt = "Change the input parameter of example in the function docstring to be a lot more complex:\n"
            prompt += f"{item.function_header}{item.docstring}{item.examples}\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = item.answer
        elif dimension == "Example Boundary":
            prompt = "Change the demostration example in the function docstring to include special input and boundary cases:\n"
            prompt += f"{item.function_header}{item.docstring}{item.examples}\n"
            output = model(prompt)
            item.function_header = output
            item.docstring = ""
            item.examples = ""
            item.answer = item.answer
        else:
            print(dimension, " Not Implemented")
            pass

        return item


if __name__ == "__main__":
    l = Ontoloty().gsm8k_question_list()
    for o in l:
        print(o.context + " " + o.question + " " + o.answer)

    l = Ontoloty().human_eval_question_list()
    for o in l:
        print(o.function_header + o.docstring + o.examples + o.answer + o.test_case)
