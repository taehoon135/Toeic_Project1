import pandas as pd

# 파일 읽기 – 인코딩 문제가 있을 경우 encoding="utf-8-sig"를 사용합니다.
df = pd.read_csv("toeic_word_updated.csv", encoding="utf-8-sig")

def assign_part_of_speech(word, meaning):
    lw = word.lower()
    # -ly로 끝나면 부사로 처리
    if lw.endswith("ly"):
        return "adv. 부사"
    # 동사로 자주 쓰이는 단어들
    elif lw in ["abandon", "abolish", "accept", "accomplish", "accompany", "address", "adjust", "alter", "announce", "appoint", "assist", "apply", "assign", "repair", "replace", "run", "deliver", "invest", "manage", "support", "yield"]:
        return "v. 동사"
    # 명사로 자주 쓰이는 단어들
    elif lw in ["ability", "absence", "account", "achievement", "acquisition", "accomplishment", "agenda", "analysis", "applicant", "assessment", "benefit", "capacity", "delivery", "development", "idea", "impact", "income", "industry", "information", "issue", "loss", "object", "result", "reward", "security"]:
        return "n. 명사"
    # 형용사로 자주 쓰이는 단어들
    elif lw in ["absolute", "abstract", "acceptable", "active", "advanced", "adequate", "aggressive", "annual", "beneficial", "brilliant", "certain", "comfortable", "creative", "critical", "efficient", "elegant", "essential", "famous", "fragile", "ideal", "incredible", "interesting", "intelligent", "logical", "modern", "pleasant", "powerful", "remarkable", "reliable", "simple", "stylish", "successful", "unusual"]:
        return "adj. 형용사"
    else:
        # 기본값은 명사로 처리
        return "n. 명사"

def generate_example_sentence(word):
    examples = {
        "abandon": "He decided to abandon his project due to a lack of funds.",
        "ability": "She has the ability to speak three languages fluently.",
        "abolish": "The government decided to abolish the outdated law.",
        "absence": "His long absence from work raised concerns among his colleagues.",
        "absolute": "Her decision was based on absolute confidence in her abilities.",
        "absolutely": "She was absolutely convinced that her decision was the best.",
        "abstract": "Her abstract ideas left the audience puzzled.",
        "accept": "They gladly accepted the invitation after careful consideration.",
        "acceptable": "The proposal was acceptable to the board.",
        "access": "The system provides secure access to all members.",
        "accessible": "The museum is fully accessible to everyone.",
        "accidentally": "He accidentally triggered the alarm.",
        "acclaim": "The film received widespread acclaim.",
        "accommodate": "The venue can accommodate a large number of guests.",
        "accompany": "She asked him to accompany her to the meeting.",
        "accomplish": "They struggled to accomplish the task before the deadline.",
        "accomplished": "He is an accomplished professional in his field.",
        "accomplishment": "Winning the award was a significant accomplishment.",
        "according to": "According to experts, the trend will continue.",
        "account": "She opened a new account at the bank.",
        # (필요에 따라 추가 단어 예문 확장 가능)
    }
    return examples.get(word.lower(), f"This is an example sentence using the word '{word}'.")

# part_of_speech가 채워져 있지 않은 경우 자동으로 채웁니다.
df["part_of_speech"] = df.apply(
    lambda row: row["part_of_speech"] if pd.notnull(row["part_of_speech"]) and str(row["part_of_speech"]).strip() != ""
                else assign_part_of_speech(row["english_word"], row["meaning"]),
    axis=1
)

# example_sentence가 채워져 있지 않은 경우 자동으로 채웁니다.
df["example_sentence"] = df.apply(
    lambda row: row["example_sentence"] if pd.notnull(row["example_sentence"]) and str(row["example_sentence"]).strip() != ""
                 else generate_example_sentence(row["english_word"]),
    axis=1
)

# 전체 데이터를 toeic_word_completed.csv 파일로 저장합니다.
df.to_csv("toeic_word_completed.csv", index=False, encoding="utf-8-sig")
print("CSV 파일 'toeic_word_completed.csv'가 생성되었습니다.")
