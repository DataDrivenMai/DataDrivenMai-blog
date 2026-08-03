"""
Description: Essential code to transliterate Japanese words written in hiragana or katakana into the Roman alphabet using `jaconv` or `pykakasi` Python libraries.
"""

# Import libraries
import jaconv
import pykakasi

# Constants
# Collection of Japanese words [Tokyo, Osaka, Pokemon, sushi, ramen] in hiragana, full-width and half-width katakana
hiragana_text = ["とうきょう", "おおさか", "ぽけもん", "すし", "らーめん"]
fw_katakana_text = ["トウキョウ", "オオサカ", "ポケモン", "スシ", "ラーメン"]
hw_katakana_text = ["ﾄｳｷｮｳ", "ｷｮｳﾄ", "ｵｵｻｶ", "ﾎﾟｹﾓﾝ", "ｽｼ", "ﾗｰﾒﾝ"] 
    
# Local functions


# Main script
def main():
    """Main script that transliterates Japanese words written in hiragana or katakana into the Roman alphabet using `jaconv` or `pykakasi`."""
    
    # Make a pykakasi.kakasi 
    kks = pykakasi.kakasi()

    # Hiragana romanization
    print('Hiragana Transliteration')

    # Work through each text item
    for hiragana_now in hiragana_text:

        # Starting hiragana
        print(hiragana_now, " converts to")

        # Convert using jaconv
        jaconv_hiragana = jaconv.kana2alphabet(hiragana_now)
        print(f'\t {jaconv_hiragana:<14} jaconv')

        # Convert using pykakasi
        kks_result = kks.convert(hiragana_now)[0]
        print(f'\t {kks_result['hepburn']:<14} pykakasi - hepburn')
        print(f'\t {kks_result['kunrei']:<14} pykakasi - kunrei')
        print(f'\t {kks_result['passport']:<14} pykakasi - passport')

    # Full-width katakana
    print('\nFull-width Katakana Transliteration')

    # Work through each text item
    for katakana_now in fw_katakana_text:

        # Starting katakana
        print(katakana_now, " converts to")

        # Convert using jaconv
        jaconv_hiragana = jaconv.kata2alphabet(katakana_now)
        print(f'\t {jaconv_hiragana:<14} jaconv')

        # Convert using pykakasi
        kks_result = kks.convert(katakana_now)[0]
        print(f'\t {kks_result['hepburn']:<14} pykakasi - hepburn')
        print(f'\t {kks_result['kunrei']:<14} pykakasi - kunrei')
        print(f'\t {kks_result['passport']:<14} pykakasi - passport')
    
    # Half-width katakana conversion
    print('\nHalf-width Katakana Transliteration requires conversion to full-width katakana first')

    # Work through each text item
    for katakana_now in hw_katakana_text:

        # Convert from half-width to full-width katakana
        fullwidth_now = jaconv.hankaku2zenkaku(katakana_now)

        # Starting katakana
        print(katakana_now, " converts to ", fullwidth_now, " which ultimately converts to ")

        # Convert using jaconv
        jaconv_hiragana = jaconv.kata2alphabet(fullwidth_now)
        print(f'\t {jaconv_hiragana:<14} jaconv')

        # Convert using pykakasi
        kks_result = kks.convert(fullwidth_now)
        for item in kks_result:
            print(f'\t {item['hepburn']:<14} pykakasi - hepburn')
        for item in kks_result:
            print(f'\t {item['kunrei']:<14} pykakasi - kunrei')
        for item in kks_result:
            print(f'\t {item['passport']:<14} pykakasi - passport')
            

if __name__ == "__main__":
    main()
