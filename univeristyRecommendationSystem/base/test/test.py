file_path = 'C:/Users/LIKHIT/Documents/SLU/PSD/Universityrecommendation/base/static/adminResources/models/Model_USA.sav'

with open(file_path, 'rb') as f:
    content = f.read(16)  # Read first 16 bytes
print(content)
