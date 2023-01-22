class ProtLoader:
    def __init__(self, file):
        self.prot = ""
        self.name = ""
        self.process(file)

    def process(self, file):
        # TODO verify file path
        with open(file, "r") as f:
            p = f.read()

        self.name = file.split("/")[-1]
        self.prot = p.replace("\n", "")


if __name__ == "__main__":
    p = ProtLoader("data/Q555C6")
    print(f"Prot {p.name} start: {p.prot[:30]}")
