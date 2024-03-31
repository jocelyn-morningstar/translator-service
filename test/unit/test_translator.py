from src.translator import translate_content


def test_chinese():
    print("Running test_chinese")
    is_english, translated_content = translate_content("这是一条中文消息")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False
    assert translated_content == "This is a Chinese message."

def test_llm_normal_response():
    print("Running first test for llm_normal_response")
    is_english, translated_content = translate_content("En un día soleado, las flores bailan con el viento en el jardín.")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False
    assert translated_content == "On a sunny day, the flowers dance with the wind in the garden."

    print("Running second test for llm_normal_response")
    is_english, translated_content = translate_content("This is English.")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == True
    assert translated_content == "This is English."

    print("Running third test for llm_normal_response")
    is_english, translated_content = translate_content("في غروب الشمس، يتلألأ سطح الماء بألوان الطيف.")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False
    assert translated_content == "At sunset, the surface of the water sparkles with rainbow colors."

    print("Running fourth test for llm_normal_response")
    is_english, translated_content = translate_content("Sur la plage déserte, le bruit des vagues apaise l'esprit.")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False
    assert translated_content == "On the deserted beach, the sound of the waves soothes the mind."


def test_llm_gibberish_response():
    print("Running first test for llm_gibberish_response")
    is_english, translated_content = translate_content("laksjdf gjoeiw giewaihfoiah hello aouhrfa")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False

    print("Running second test for llm_gibberish_response")
    is_english, translated_content = translate_content("932509 594072 76049724 59")
    print("Is English? ", is_english)
    print("returned string: ", translated_content)
    assert is_english == False
