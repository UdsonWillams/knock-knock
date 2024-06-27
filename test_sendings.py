from uknockknock import desktop_sender
from uknockknock import FunctionModel

model = FunctionModel(
    date_format="%d-%m-%Y %H:%M:%S",
    final_text_message="testando!"
)

@desktop_sender(title="Tomar remedio!", model=model)
def take_medicine_at_5():
    import time
    time.sleep(5)
    return {"loss": 0.9}

if __name__ == "__main__":
    take_medicine_at_5()
