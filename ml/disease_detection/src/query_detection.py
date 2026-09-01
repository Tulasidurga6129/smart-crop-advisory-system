import sys

from src.data_loader import get_class_names
from src.recommendations import get_recommendation


def normalize_text(text):
    return (
        text.lower()
        .replace("_", " ")
        .replace("-", " ")
        .strip()
    )


def detect_disease_from_query(query):

    query = normalize_text(query)

    class_names = get_class_names()

    keyword_map = {

        "Pepper__bell___Bacterial_spot": [
            "pepper bacterial spot",
            "pepper bacterial",
            "pepper dark spots",
            "pepper spots",
            "bacterial spot pepper",
        ],

        "Pepper__bell___healthy": [
            "pepper healthy",
            "healthy pepper",
            "pepper no disease",
        ],

        "Potato___Early_blight": [
            "potato early blight",
            "potato early",
            "early blight potato",
        ],

        "Potato___Late_blight": [
            "potato late blight",
            "potato late",
            "late blight potato",
        ],

        "Potato___healthy": [
            "potato healthy",
            "healthy potato",
            "potato no disease",
        ],

        "Tomato_Bacterial_spot": [
            "tomato bacterial spot",
            "tomato bacterial",
            "bacterial spot tomato",
        ],

        "Tomato_Early_blight": [
            "tomato early blight",
            "tomato early",
            "early blight tomato",
        ],

        "Tomato_Late_blight": [
            "tomato late blight",
            "tomato late",
            "late blight tomato",
        ],

        "Tomato_Leaf_Mold": [
            "tomato leaf mold",
            "tomato leaf mould",
            "leaf mold tomato",
            "leaf mould tomato",
        ],

        "Tomato_Septoria_leaf_spot": [
            "tomato septoria",
            "septoria leaf spot",
            "tomato septoria leaf spot",
        ],

        "Tomato_Spider_mites_Two_spotted_spider_mite": [
            "tomato spider mites",
            "tomato spider mite",
            "spider mites tomato",
            "two spotted spider mite",
            "spider mite tomato",
        ],

        "Tomato__Target_Spot": [
            "tomato target spot",
            "target spot tomato",
        ],

        "Tomato__Tomato_YellowLeaf__Curl_Virus": [
            "tomato yellow leaf curl",
            "yellow leaf curl virus",
            "tomato yellow leaf curl virus",
            "tomato leaf curl",
        ],

        "Tomato__Tomato_mosaic_virus": [
            "tomato mosaic virus",
            "tomato mosaic",
            "mosaic virus tomato",
        ],

        "Tomato_healthy": [
            "tomato healthy",
            "healthy tomato",
            "tomato no disease",
        ],
    }
    best_class = None
    best_score = 0

    for class_name in class_names:

        keywords = keyword_map.get(
            class_name,
            []
        )

        score = 0

        for keyword in keywords:

            # Exact phrase match
            if keyword in query:
                score += len(keyword.split()) * 2

            # Individual word matching
            else:
                keyword_words = keyword.split()

                matched_words = sum(
                    1
                    for word in keyword_words
                    if word in query
                )

                score += matched_words

        if score > best_score:
            best_score = score
            best_class = class_name

    if best_class is None:
        return None

    recommendation = get_recommendation(
        best_class
    )

    return {
        "class_name": best_class,
        "plant": recommendation["plant"],
        "disease": recommendation["disease"],
        "description": recommendation["description"],
        "treatment": recommendation["treatment"],
        "fertilizer": recommendation["fertilizer"],
        "prevention": recommendation["prevention"],
    }


def main():

    if len(sys.argv) < 2:

        print()
        print("Usage:")
        print(
            'python -m src.query_detection "your symptoms"'
        )
        return

    query = " ".join(sys.argv[1:])

    print()
    print("========================================")
    print("       QUERY DISEASE DETECTION")
    print("========================================")
    print()

    print(f"Query: {query}")
    print()

    try:

        result = detect_disease_from_query(query)

        if result is None:

            print("No matching disease was found.")
            print()
            print(
                "Try including the crop name and "
                "disease/symptom."
            )
            print()
            return

        print("========== QUERY RESULT ==========")
        print()

        print(
            f"Plant   : {result['plant']}"
        )

        print(
            f"Disease : {result['disease']}"
        )

        print()

        print(
            "========== DISEASE INFORMATION =========="
        )

        print(result["description"])
        print()

        print("========== TREATMENT ==========")

        for item in result["treatment"]:
            print(f"- {item}")

        print()

        print(
            "========== FERTILIZER / NUTRIENTS =========="
        )

        print(result["fertilizer"])
        print()

        print("========== PREVENTION ==========")

        for item in result["prevention"]:
            print(f"- {item}")

        print()
        print("========================================")

    except Exception as e:

        print()
        print("Query detection failed.")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()