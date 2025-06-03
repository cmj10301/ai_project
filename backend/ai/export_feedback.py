from backend.mongoDBConnect import feedback_collection
import json

def export_for_finetune(json_path='feedback_data.json'):
    cursor = feedback_collection.find({
        "is_correct": False,
        "correct_label": {"$exists": True}
    })

    export_data = []
    for doc in cursor:
        export_data.append({
            "image_base64": doc["image_base64"],
            "label": doc["correct_label"]
        })

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(export_data)} entries to {json_path}")
