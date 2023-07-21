from datetime import timedelta

def caluculate_diapason(date_now, diapason: int) -> tuple:
    # Вычисляем стартовое время например, если 11:44, то стартовое время 11:40
    correct_diapason = diapason + date_now.minute % 10
    start_time = date_now - timedelta(hours=0, minutes=correct_diapason)
    end_time = start_time + timedelta(hours=0, minutes=diapason)
    print('Диапазон', start_time, end_time)
    return start_time, end_time