import os
import pandas as pd
from PyPDF2 import PdfReader
from PIL import Image


BASE_DIR = "/mnt/data/extracted_export"
CSV_PATH = os.path.join(BASE_DIR, "MMdashboard 216b50e66dba80e6b324fe49e1b68b52", "Topic DB 216b50e66dba805abdb2ebd9cbd601da.csv")
PDF_PATH = os.path.join(BASE_DIR, "Book_1 225b50e66dba80a8b9e6d7530c2e8cf5.pdf")
IMG_PATH = os.path.join(BASE_DIR, "Book_1 225b50e66dba80a8b9e6d7530c2e8cf5", "Untitled_design.png")


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file and print a brief summary."""
    print("\n📄 CSV 파일 로드 중...")
    df = pd.read_csv(path)
    print("열 이름:", df.columns.tolist())
    print("데이터 개수:", len(df))
    print("상위 5개 행:")
    print(df.head())
    return df


def summarize_pdf(path: str) -> None:
    """Print PDF metadata and the first page preview."""
    print("\n📚 PDF 요약 정보:")
    reader = PdfReader(path)
    print(f"총 페이지 수: {len(reader.pages)}")
    if reader.pages:
        print("첫 페이지 미리보기:")
        print(reader.pages[0].extract_text())


def summarize_image(path: str) -> None:
    """Display basic information about an image file."""
    print("\n🖼️ 이미지 파일 정보:")
    img = Image.open(path)
    print(f"이미지 크기: {img.size}")
    img.show()


def list_all_files(directory: str, output: str = "file_list.txt") -> None:
    """Save a listing of all files under ``directory`` to ``output``."""
    print("\n📁 폴더 내 모든 파일 목록 저장 중...")
    with open(output, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(directory):
            for file in files:
                full_path = os.path.join(root, file)
                f.write(full_path + "\n")
    print(f"모든 파일 목록이 '{output}'에 저장되었습니다.")


def main() -> None:
    print("==== 데이터 관리 프로그램 시작 ====")
    df = load_csv(CSV_PATH)
    summarize_pdf(PDF_PATH)
    summarize_image(IMG_PATH)
    list_all_files(BASE_DIR)
    print("==== 프로그램 종료 ====")


if __name__ == "__main__":
    main()
