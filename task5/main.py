from task5.editor import TextEditor


def main():

    editor = TextEditor()

    print("=== Демонстрація текстового редактора з Memento ===\n")

    print(f"Початковий вміст: '{editor.get_content()}'")

    editor.write_text("Привіт, світ!")
    print(f"Після запису: '{editor.get_content()}'")

    editor.append_text(" Це тестовий документ.")
    print(f"Після додавання: '{editor.get_content()}'")

    editor.append_text(" Додамо ще трохи тексту.")
    print(f"Після другого додавання: '{editor.get_content()}'")

    print(f"\nМожна скасувати: {editor.can_undo()}")

    editor.undo()
    print(f"Після undo: '{editor.get_content()}'")

    editor.undo()
    print(f"Після другого undo: '{editor.get_content()}'")

    print(f"\nМожна повторити: {editor.can_redo()}")

    editor.redo()
    print(f"Після redo: '{editor.get_content()}'")

    editor.write_text("Новий текст після undo")
    print(f"Новий текст: '{editor.get_content()}'")
    print(f"Можна повторити після нової зміни: {editor.can_redo()}")

    print(f"\nІсторія змін:")
    for i, info in enumerate(editor.get_history_info()):
        print(f"  {i}: {info['timestamp'].strftime('%H:%M:%S')} - "
              f"довжина: {info['content_length']}, "
              f"попередній перегляд: '{info['preview']}'")

    print(f"\nІнформація про документ:")
    doc_info = editor.get_document_info()
    print(f"  Довжина: {doc_info['length']} символів")
    print(f"  Створено: {doc_info['created_at'].strftime('%H:%M:%S')}")
    print(f"  Змінено: {doc_info['modified_at'].strftime('%H:%M:%S')}")


if __name__ == "__main__":
    main()