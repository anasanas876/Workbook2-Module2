import filetype
from pypdf import PdfReader

file_path = input("Enter your File Path: ")
print(repr(file_path))
try:
    check_file_path = filetype.guess(file_path)

    if check_file_path is None:
        print("Not a valid file")

    else:
        print(check_file_path)

        extension = check_file_path.extension
        mime = check_file_path.mime

        if extension in ("pdf", "docx"):
            print(f"File type is {extension}")

            if extension == "pdf":
                reader = PdfReader(file_path)
                for page in reader.pages:
                    text=page.extract_text()
                    print(text)
                    

        else:
            print("Not supported file type for Resume")

except FileNotFoundError:
    print("The path entered does not exist.")