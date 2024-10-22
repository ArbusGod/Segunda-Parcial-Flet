import flet as ft
import os

# Función principal que configura la página
def main(page: ft.Page):
    # Establecemos el color de fondo de la página a un verde oscuro (#34495e)
    page.bgcolor = "#34495e"  # Color de fondo verde oscuro

    # Definimos una lista para almacenar los ítems de la lista de compras
    shopping_list = []

    # Ruta del logo de la aplicación, que será una imagen
    logo_path = os.path.join(os.path.dirname(__file__), "image/logo1.png")
    logo = ft.Image(src=logo_path, width=200, height=150)

    # Definimos el ancho y alto de la aplicación
    page.window_width = 600  # Ancho de la ventana cambiado a 600px
    page.window_height = 400  # Alto de la ventana cambiado a 400px
    page.title = "Lista de Compras"  # Título de la aplicación

    #para centrar todo y hacer un calculo del tamaño de la pantalla y centrar la ventana
    page.horizontal_alignment = "center"  # Alineación horizontal del contenido
    screen_width = 1920
    screen_height = 1080

    # Calculamos la posición para centrar la ventana
    page.window_left = (screen_width - page.window_width) // 2.5  # Posición horizontal
    page.window_top = (screen_height - page.window_height) // 3  # Posición vertical
    # Función para mostrar un mensaje de bienvenida al iniciar la aplicación
    def show_welcome_dialog():
        def close_welcome_dlg(e):
            page.dialog.open = False  # Cierra el diálogo de bienvenida
            page.update()  # Actualiza la página

        # Cuadro de diálogo con el mensaje de bienvenida
        page.dialog = ft.AlertDialog(
            title=ft.Text("Bienvenido"),
            content=ft.Text("Bienvenido a tu App de Lista de Compras. ¡No te olvides de nada!"),
            actions=[ft.TextButton("OK", on_click=close_welcome_dlg)],  # Botón para cerrar el mensaje de bienvenida
            open=True
        )
        page.update()  # Actualiza la página para mostrar el cuadro de diálogo

    # Función que muestra un cuadro de diálogo de error si se intenta agregar un ítem vacío
    def show_error_dialog():
        def close_dlg(e):
            dialog.open = False  # Cerrar el diálogo
            page.update()  # Actualizar la página

        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text("No puedes agregar un ítem en blanco."),
            actions=[ft.TextButton("OK", on_click=close_dlg)],
            open=True
        )
        page.overlay.append(dialog)  # Usar overlay para mostrar el diálogo
        page.update()

    # Función que se ejecuta cuando el botón "Agregar" es presionado
    def add_clicked(e):
        # Verifica que el campo de texto no esté vacío
        if not new_task.value.strip():  # Si el campo está vacío, muestra el error
            show_error_dialog()  # Llama a la función para mostrar el error
            return

        # Crea un nuevo ítem y lo añade a la lista si el campo de texto no está vacío
        item = create_item(new_task.value)
        shopping_list.append(new_task.value)  # Añade el nuevo ítem a la lista de compras
        page.add(item)  # Añade el ítem visualmente a la página
        new_task.value = ""  # Limpia el campo de texto
        new_task.focus()  # Devuelve el foco al campo de texto

        # Actualiza los controles para mostrar el botón de exportar si hay ítems en la lista
        update_buttons()

    # Función que crea un ítem visual con un checkbox, un botón de editar y uno de eliminar
    def create_item(text):
        checkbox = ft.Checkbox(label=text)  # Checkbox con el nombre del ítem
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, text))
        item = ft.Row([checkbox, edit_button, delete_button])  # Crea una fila con los elementos del ítem
        return item

    # Función que permite editar un ítem
    def edit_clicked(e, checkbox, item):
        new_value = ft.TextField(value=checkbox.label, width=300)  # Campo de texto para editar el ítem
        save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=lambda e: save_clicked(e, checkbox, new_value, item))
        cancel_button = ft.IconButton(icon=ft.icons.CANCEL, on_click=lambda e: cancel_clicked(e, checkbox, item))
        item.controls = [new_value, save_button, cancel_button]  # Reemplaza los controles del ítem con los de edición
        page.update()  # Actualiza la página

    # Función que guarda los cambios realizados al editar un ítem
    def save_clicked(e, checkbox, new_value, item):
        checkbox.label = new_value.value  # Actualiza el texto del checkbox con el nuevo valor
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]  # Vuelve a mostrar los controles originales del ítem
        page.update()  # Actualiza la página

    # Función que cancela la edición de un ítem
    def cancel_clicked(e, checkbox, item):
        edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=lambda e: edit_clicked(e, checkbox, item))
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e: delete_clicked(e, item, checkbox.label))
        item.controls = [checkbox, edit_button, delete_button]  # Vuelve a mostrar los controles originales del ítem
        page.update()  # Actualiza la página

    # Función que elimina un ítem de la lista
    def delete_clicked(e, item, text):
        shopping_list.remove(text)  # Remueve el ítem de la lista de compras
        page.controls.remove(item)  # Remueve visualmente el ítem de la página
        page.update()  # Actualiza la página
        update_buttons()  # Actualiza los botones si la lista está vacía

    # Función que exporta la lista de compras a un archivo de texto (.txt)
    def export_list(e):
        if shopping_list:  # Verifica que la lista no esté vacía antes de exportar
            file_path = "lista_de_compras.txt"  # Ruta del archivo
            # Escribe los ítems en un archivo de texto
            with open(file_path, "w") as file:
                for item in shopping_list:
                    file.write(f"{item}\n")  # Añade cada ítem como una nueva línea en el archivo

            # Muestra un cuadro de diálogo con un enlace para descargar el archivo
            download_link = ft.TextButton("Descargar archivo", on_click=lambda e: page.launch_url(f"/{file_path}"))
            page.dialog = ft.AlertDialog(
                title=ft.Text("Éxito"),
                content=ft.Text("Haz clic en el siguiente enlace para descargar la lista:"),  # Mensaje de éxito
                actions=[download_link],  # Enlace para descargar el archivo
                open=True
            )
            page.update()  # Actualiza la página

    # Función que actualiza los botones de agregar y exportar
    def update_buttons():
        button_row.controls = [
            new_task,  # Campo de entrada para un nuevo ítem
            ft.ElevatedButton("Agregar", on_click=add_clicked),  # Botón de agregar ítem
        ]

        # Si la lista no está vacía, añade el botón de exportar lista
        if shopping_list:
            button_row.controls.append(ft.ElevatedButton("Exportar Lista a .txt", on_click=export_list))
        
        page.update()  # Actualiza la página para reflejar los cambios

    # Campo de entrada para añadir un nuevo ítem a la lista
    new_task = ft.TextField(hint_text="¿Qué necesitas comprar?", width=250)
    
    # Texto de cabecera con el logo de la aplicación y mensaje de bienvenida
    header_text = ft.Text("Añade todo lo que tengas que traer aquí abajo", size=20, weight=ft.FontWeight.BOLD)


    # Organiza la cabecera en una columna centrada
    header = ft.Column(
    [logo, header_text], 
    alignment=ft.MainAxisAlignment.CENTER, 
    horizontal_alignment=ft.CrossAxisAlignment.CENTER
)

# Fila que contiene el campo de entrada y el botón de agregar
    button_row = ft.Row(
    [new_task, ft.ElevatedButton("Agregar", on_click=add_clicked)], 
    alignment=ft.MainAxisAlignment.CENTER
)

# Columna que contiene los ítems de la lista de compras
    list_column = ft.Column(
    expand=True,  # Permite que la lista se expanda conforme se agregan ítems
    scroll=ft.ScrollMode.AUTO,  # Añade un scrollbar si la lista crece más allá del espacio disponible
)

# Columna principal que contiene todos los elementos
    main_column = ft.Column(
    [header, ft.Divider(height=20), button_row, list_column], 
    alignment=ft.MainAxisAlignment.START,  # Asegura que el contenido se alinee desde la parte superior
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    expand=True  # Para que se ajuste a la ventana
)
    # Añadimos los elementos principales a la página
    page.add(
        header,  # Cabecera con el logo y el mensaje
        ft.Divider(height=20),  # Separador entre la cabecera y los botones
        button_row  # Fila de botones y campo de entrada
    )

    # Muestra el mensaje de bienvenida al cargar la página
    show_welcome_dialog()

# Ejecuta la aplicación Flet
ft.app(target=main)
