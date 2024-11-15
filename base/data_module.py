import pandas as pd
from sklearn.preprocessing import LabelEncoder


def write_data():
    # Load the dataset
    acedamic_dataframe = pd.read_excel(
        r'C:\projectworkspace\universityrecommendation\base\static\adminResources\dataset\Dataset_AUS.xlsx'
    )

    # Write to the txt file
    txt_file = open(r"C:\projectworkspace\universityrecommendation\base\static\adminResources\australia_classes.txt",
                    "w")

    # Initialize the LabelEncoder
    label_encoder = LabelEncoder()

    # Transform the 'UNIVERSITY' column into numeric values
    y = label_encoder.fit_transform(acedamic_dataframe['UNIVERSITY'])

    for x in range(len(acedamic_dataframe['UNIVERSITY'])):
        college_name = acedamic_dataframe['UNIVERSITY'][x]
        college_id = y[x]
        txt_file.write(college_name.replace(" ", "_") + " " + str(college_id) + "\n")

    txt_file.close()


def read_data(college_id):
    # Read the txt file with the class mappings
    txt_file = open(r"C:\projectworkspace\universityrecommendation\base\static\adminResources\australia_classes.txt",
                    "r")
    data_dict = {}

    # Read each line and split by space to populate the dictionary
    data_list = txt_file.readlines()
    for i in data_list:
        data = i.replace("\n", "").split(" ")
        data_dict.update({int(data[1]): data[0]})

    value_data = data_dict.get(college_id)
    txt_file.close()

    return value_data


# To run the write_data function when this script is executed
if __name__ == "__main__":
    write_data()
