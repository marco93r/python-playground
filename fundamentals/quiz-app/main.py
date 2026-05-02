questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Paris", "Madrid", "Rome"],
        "answer": 2
    },
    {
        "question": "What is the capital of Austria?",
        "options": ["Berlin", "Paris", "Madrid", "Vienna"],
        "answer": 4
    },
    {
        "question": "What color has the sky?",
        "options": ["Blue", "Green", "Yellow", "Purple"],
        "answer": 1
    }
]

def main():
    score = 0
    number_questions = 0
    for q in questions:
        number_questions += 1
        print(q['question'])
        print(*q['options'])
        while True:
            answer = input("Answer 1, 2, 3 or 4: ")
            if answer.isdigit() and 1 <= int(answer) <= 4:
                break
            print('Invalid input!')
            
        if int(answer) == q['answer']:
            score += 1
        else:
            print('Wrong answer, correct:', q['options'][q['answer'] - 1])
                

    print('You got', score, '/', number_questions, 'correct!')

main()

