CREATE = "create"
REMOVE = "remove"
LIST = "list"
PROBABILITY = "probability"
RECOMMENDATION = "recommendation"


class Patient:
    def __init__(self, name, diagnosis_accuracy, disease_name, incidence, treatment_name, treatment_risk):
        self.name = name
        self.diagnosis_accuracy = float(diagnosis_accuracy)
        self.disease_name = disease_name
        self.incidence = incidence
        self.treatment_name = treatment_name
        self.treatment_risk = float(treatment_risk)

    def disease_probability(self):
        positive, total = map(float, self.incidence.split("/"))
        denominator = ((1 - self.diagnosis_accuracy) * (total - positive)) + positive
        return (positive / denominator) * 100

    def recommendation(self):
        return self.disease_probability() >= self.treatment_risk * 100


class DoctorsAid:
    def __init__(self):
        self.patients = {}

    def create_patient(self, parts, output):
        name = parts[1]

        if name in self.patients:
            output.write(f"Patient {name} cannot be recorded due to duplication.\n")
            return

        diagnosis_accuracy = parts[2]
        disease_name = parts[3] + " " + parts[4]
        incidence = parts[5]

        if len(parts) == 9:
            treatment_name = parts[6] + " " + parts[7]
            treatment_risk = parts[8]
        else:
            treatment_name = parts[6]
            treatment_risk = parts[7]

        self.patients[name] = Patient(
            name, diagnosis_accuracy, disease_name, incidence, treatment_name, treatment_risk
        )
        output.write(f"Patient {name} is recorded.\n")

    def remove_patient(self, name, output):
        if name not in self.patients:
            output.write(f"Patient {name} cannot be removed due to absence.\n")
            return

        del self.patients[name]
        output.write(f"Patient {name} is removed.\n")

    def list_patients(self, output):
        output.write("Patient\tDiagnosis\tDisease\tIncidence\tTreatment\tRisk\n")
        output.write("-" * 80 + "\n")

        for patient in self.patients.values():
            accuracy = f"{patient.diagnosis_accuracy * 100:.2f}%"
            risk = f"{round(patient.treatment_risk * 100)}%"
            output.write(
                f"{patient.name}\t{accuracy}\t{patient.disease_name}\t"
                f"{patient.incidence}\t{patient.treatment_name}\t{risk}\n"
            )

    def calculate_probability(self, name, output):
        if name not in self.patients:
            output.write(f"Probability for {name} cannot be calculated due to absence.\n")
            return

        patient = self.patients[name]
        probability = patient.disease_probability()
        output.write(
            f"Patient {name} has a probability of {probability:.2f}% "
            f"of having {patient.disease_name}.\n"
        )

    def make_recommendation(self, name, output):
        if name not in self.patients:
            output.write(f"Recommendation for {name} cannot be calculated due to absence.\n")
            return

        patient = self.patients[name]
        if patient.recommendation():
            output.write(f"System suggests {name} to have the treatment.\n")
        else:
            output.write(f"System suggests {name} NOT to have the treatment.\n")


def parse_line(line):
    return line.strip().replace(" ", ",").replace(",,", ",").split(",")


def main():
    system = DoctorsAid()

    with open("doctors_aid_inputs.txt", "r", encoding="utf-8") as input_file, open(
        "outputs.txt", "w", encoding="utf-8"
    ) as output_file:
        for line in input_file:
            if not line.strip():
                continue

            parts = parse_line(line)
            command = parts[0]

            if command == CREATE:
                system.create_patient(parts, output_file)
            elif command == REMOVE:
                system.remove_patient(parts[1], output_file)
            elif command == LIST:
                system.list_patients(output_file)
            elif command == PROBABILITY:
                system.calculate_probability(parts[1], output_file)
            elif command == RECOMMENDATION:
                system.make_recommendation(parts[1], output_file)


if __name__ == "__main__":
    main()
