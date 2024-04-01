from src.translator import translate_content, client
from openai import RateLimitError
from time import sleep

try:
    from numpy import dot
except ImportError:
    def dot(a, b):
        assert(len(a) == len(b))
        n = len(a)
        numerator = sum([a[i] * b[i] for i in range(n)])
        denominator = sum([a[i] ** 2 for i in range(n)]) * sum([b[i] ** 2 for i in range(n)])
        return numerator / denominator

class Tester:
    def __init__(self, verbose=True, simple=False) -> None:
        self.tests = []
        self.verbose = verbose #If false, testing will print less often. 
        self.simple = simple #If true, we do a simple string comparison instead of using cosine_similarity
        self.model = "text-embedding-3-small"
        
    def queue_test(self, content, englishness, real_translation):
        self.tests.append((content, englishness, real_translation))
        
    def compare(self, englishness, actual, expected, tolerance=0.07, simple=False) -> 'bool':
        if self.simple or simple or englishness:
            return actual == expected
        
        sleep(5)
        val = client.embeddings.create(input=[actual, expected], model=self.model)
        embedding1 = val.data[0].embedding
        embedding2 = val.data[1].embedding
        
        similarity = dot(embedding1, embedding2)
        if (self.verbose):
            print(f"Similarity: {similarity}")
        
        return abs(1 - similarity) < tolerance
        
    def run_test(self, content, englishness, real_translation) -> 'bool':
        is_english, translated_content = translate_content(content)
        
        if self.verbose:
            print(f"Is English? {is_english} (expected: {englishness})")
            print(f"Returned string: {translated_content} (expected: {real_translation})")
        
        result = (is_english == englishness) and self.compare(englishness, real_translation, translated_content)
        return result
        
    def run_all_queued_tests(self):
        num_tests = len(self.tests)
        passed_tests = 0
        for i, (a, b, c) in enumerate(self.tests):
            print(f"Running test {i}/{num_tests}")
            
            try:
                if self.run_test(a, b, c): 
                    passed_tests += 1
                    print("PASSED!")
                    
            except RateLimitError:
                print("A rate limit error occurred. Pausing tests for 30 seconds...")
                sleep(30)
                
                if self.run_test(a, b, c): 
                    passed_tests += 1
                    print("PASSED!")
                
            
        print(f"Test suite complete. ({passed_tests} / {num_tests}) PASSED.")
        assert (passed_tests == num_tests)
        
    def single_test(self, content, englishness, real_translation):
        assert self.run_test(content, englishness, real_translation)

def one_test(content, englishness, real_translation, verbose=True):
    is_english, translated_content = translate_content(content)
    
    if verbose:
        print(f"Is English? {is_english} (expected: {englishness})")
        print(f"Returned string: {translated_content} (expected: {real_translation})")
    
    result = (is_english == englishness) and (translated_content == real_translation)
    return result

def test_chinese():
    print("Running test_chinese")
    Tester().single_test("这是一条中文消息", False, "This is a Chinese message.")

def test_llm_normal_response():
    print("Running tests on proper recognition of non-English & valid translation.")
    tester = Tester()
    
    tester.queue_test(
        "En un día soleado, las flores bailan con el viento en el jardín.",
        False,
        "On a sunny day, the flowers dance with the wind in the garden."
    )
    
    tester.queue_test(
        "Estoy listo.",
        False,
        "I am ready."
    )
    
    tester.queue_test(
        "Lo tengo aquí.",
        False,
        "I have it here."
    )
    
    tester.queue_test(
        "في غروب الشمس، يتلألأ سطح الماء بألوان الطيف.",
        False,
        "At sunset, the surface of the water sparkles with rainbow colors."
    )

    tester.queue_test(
        "Sur la plage déserte, le bruit des vagues apaise l'esprit.",
        False,
        "On the deserted beach, the sound of the waves soothes the mind."
    )
    
    tester.queue_test(
        "Sur la plage déserte, le bruit des vagues apaise l'esprit.",
        False,
        "On the deserted beach, the sound of the waves soothes the mind."
    )
    
    tester.queue_test(
        "This is English.",
        True,
        "This is English."
    )
    
    tester.queue_test(
        "This is also English.",
        True,
        "This is also English."
    )
    
    tester.queue_test( #This is not a grammatically correct full sentence, but it is still English.
        "This English.",
        True,
        "This English."
    )
    
    tester.queue_test(
        "Arugula bees are imminent.",
        True,
        "Arugula bees are imminent."
    )
    
    tester.queue_test("egg", True, "egg")
    
    tester.run_all_queued_tests()
    


def test_llm_gibberish_response():
    tester = Tester(simple=True)
    
    print("Running tests for llm_gibberish_response.")
    
    tester.queue_test("laksjdf gjoeiw giewaihfoiah hello aouhrfa", False, None)
    tester.queue_test("932509 594072 76049724 59", False, None)
    tester.queue_test("516rfy2uj,1guo;y. g9p2yl ;319phkn", False, None)
    
    tester.run_all_queued_tests()

def run_all_tests():
    test_chinese()
    test_llm_normal_response()
    test_llm_gibberish_response()

if __name__ == '__main__':
   run_all_tests()