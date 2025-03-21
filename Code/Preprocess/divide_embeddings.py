import json
import os
from datetime import datetime
import pandas as pd

def divide_embeddings():
    # 폴더 경로 설정
    filedir = os.path.join(os.curdir, "./Data/Embedding")
    csvdir = os.path.join(os.curdir, "./Data/News")
    
    embedding_list = os.listdir(filedir)
    csv_list = os.listdir(csvdir)
    
    # Embedding 파일들을 순회
    for file in embedding_list:
        filepath = os.path.join(filedir, file)
        with open(filepath, mode="r", encoding="utf-8") as f:
            # JSON 파일은 리스트 형식(각 항목은 dict라고 가정)
            embeddings = json.load(f)
        
        # 파일명에서 연도 추출 (예: embedding_2023_XX.json)
        try:
            year = file.split("_")[1]
        except IndexError:
            print(f"파일명 형식이 올바르지 않습니다: {file}")
            continue
        
        # CSV 파일 리스트 중 해당 연도를 포함하는 파일 찾기
        csv_file_path = None
        for csvfile in csv_list:
            if year in csvfile:
                csv_file_path = os.path.join(csvdir, csvfile)
                break
        if not csv_file_path:
            print(f"연도 {year}에 해당하는 CSV 파일을 찾을 수 없습니다. (파일: {file})")
            continue
        
        # CSV 파일에서 ID와 Link 컬럼만 읽기
        try:
            df = pd.read_csv(csv_file_path, encoding="utf-8")[["ID", "Link"]]
        except Exception as e:
            print(f"CSV 파일 읽기 오류({csv_file_path}): {e}")
            continue
        
        # ID와 Link의 매핑 생성
        link_dict = dict(zip(df["ID"], df["Link"]))
        
        # JSON 각 레코드에 Link 컬럼 추가
        for record in embeddings:
            rec_id = record.get("original")
            record["Link"] = link_dict.get(rec_id, None)
        
        # 월별 분할: Q1: 1~3, Q2: 4~6, Q3: 7~9, Q4: 10~12
        q1, q2, q3, q4 = [], [], [], []
        for record in embeddings:
            rec_id = record.get("ID")
            if not rec_id or len(rec_id) < 6:
                print(f"유효하지 않은 ID 형식: {rec_id}")
                continue
            # ID 형식 예시: YYYYMMDD_XXX_B01S -> 월은 인덱스 4~6 (예: '01')
            try:
                month = int(rec_id[4:6])
            except ValueError:
                print(f"월 추출 실패, ID: {rec_id}")
                continue

            if 1 <= month <= 3:
                q1.append(record)
            elif 4 <= month <= 6:
                q2.append(record)
            elif 7 <= month <= 9:
                q3.append(record)
            elif 10 <= month <= 12:
                q4.append(record)
            else:
                print(f"잘못된 월 값({month})을 가진 ID: {rec_id}")

        # 저장 경로 설정 (출력 폴더 생성)
        output_dir = os.path.join(filedir, "Divided")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 원본 파일명에서 확장자를 제거하고 분할 결과 저장
        base_name = os.path.splitext(file)[0]
        output_files = {
            "Q1": os.path.join(output_dir, f"{base_name}_Q1.json"),
            "Q2": os.path.join(output_dir, f"{base_name}_Q2.json"),
            "Q3": os.path.join(output_dir, f"{base_name}_Q3.json"),
            "Q4": os.path.join(output_dir, f"{base_name}_Q4.json")
        }
        
        # 각 분할된 데이터를 JSON 파일로 저장
        with open(output_files["Q1"], "w", encoding="utf-8") as f:
            json.dump(q1, f, ensure_ascii=False, indent=4)
        with open(output_files["Q2"], "w", encoding="utf-8") as f:
            json.dump(q2, f, ensure_ascii=False, indent=4)
        with open(output_files["Q3"], "w", encoding="utf-8") as f:
            json.dump(q3, f, ensure_ascii=False, indent=4)
        with open(output_files["Q4"], "w", encoding="utf-8") as f:
            json.dump(q4, f, ensure_ascii=False, indent=4)
        
        print(f"{file} 파일은 연도 {year}에 해당하는 CSV와 병합 후 4분기로 분할하여 저장되었습니다.")

if __name__ == "__main__":
    divide_embeddings()
