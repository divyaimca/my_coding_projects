import yaml  ##pip3 install pyyaml
import os


def update_helm_chart(umbrella_chart_file,**sub_chart_name_version):
    
    try:
        with open(umbrella_chart_file) as yamlFile:
            dataMap = yaml.safe_load(yamlFile)
    except FileNotFoundError as err:
        print('file doesnot exist')
        raise err
    except IOError as err:
        print('IO Error')
        raise err


    #for i in dataMap["dependencies"]: print(i)

    for chart,version in sub_chart_name_version.items():
        for item in dataMap["dependencies"]:
            if item["name"] == chart:
                print(f'Current version of {item["name"]} is {item["version"]}')
                if item["version"] == version:
                    print(f'{chart} chart version is already found to be updated')
                else:
                    print(f'{chart} needs to be updated to {version}')
                    item["version"] = version

    
    #for i in dataMap["dependencies"]: print(i)

    newDataMap = dataMap.copy()

    try:
        with open("updatedChart.yaml","w") as yamlFile2:
            yaml.dump(newDataMap, yamlFile2) 
    except FileNotFoundError as err:
        print('file doesnot exist')
        raise err
    except IOError as err:
        print('IO Error')
        raise err

    os.rename("updatedChart.yaml", umbrella_chart_file)



def main():
    update_helm_chart("./chart.yaml",push="0.2.574",auth="0.2.585",mp="0.2.576")    


if __name__ == "__main__":
    main()
