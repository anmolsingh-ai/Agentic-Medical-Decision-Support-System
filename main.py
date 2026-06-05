from crew.symptrack_crew import SympTrackCrew
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🩺 SympTrack AI System")

    symptoms = input("Enter symptoms: ")
    age = input("Age: ")
    gender = input("Gender: ")
    city = input("City: ")

    crew = SympTrackCrew()
    result = crew.run(symptoms, age, gender, city)

    print("\n📊 RESULT:\n")
    print(result)


if __name__ == "__main__":
    main()