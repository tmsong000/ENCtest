import os
import sqlite3
import shutil
import tempfile

# 입력 디렉토리 설정
input_dir = r'C:/WORK/US_ENC_EXPORT_250724/all/ENC6118/export_gpkg'
output_folder = os.path.join(input_dir, 'results')
os.makedirs(output_folder, exist_ok=True)

# GPKG 파일 반복 처리
for filename in os.listdir(input_dir):
    if not filename.endswith(".gpkg"):
        continue

    input_file = os.path.join(input_dir, filename)
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, filename)
    shutil.copy(input_file, temp_file)

    # DATSET 값: 파일명에서 확장자 제거한 이름
    DATSET_value = os.path.splitext(filename)[0]
    escaped_value = DATSET_value.replace("'", "''")  # SQL 문자열용 이스케이프

    try:
        # SQLite 연결
        conn = sqlite3.connect(temp_file)
        cursor = conn.cursor()

        # gpkg_contents 테이블에서 공간 레이어만 추출
        cursor.execute("""
            SELECT table_name 
            FROM gpkg_contents 
            WHERE data_type IN ('features', 'tiles');
        """)
        layer_tables = [row[0] for row in cursor.fetchall()]

        for table in layer_tables:
            # 해당 테이블의 필드 목록 확인
            cursor.execute(f"PRAGMA table_info('{table}');")
            columns = [col[1] for col in cursor.fetchall()]

            # DATSET 필드가 없다면 추가
            if 'DATSET' not in columns:
                cursor.execute(f"""
                    ALTER TABLE "{table}" 
                    ADD COLUMN DATSET TEXT DEFAULT '{escaped_value}';
                """)

        conn.commit()
    except Exception as e:
        print(f"{filename} 처리 중 오류 발생: {e}")
    finally:
        conn.close()

    # 결과 파일 이동
    shutil.move(temp_file, os.path.join(output_folder, filename))
    shutil.rmtree(temp_dir)

print("작업 완료.")
