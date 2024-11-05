import flet as ft
import sqlite3 as sq
from random import choice
from datetime import datetime

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    Dialog = None
    global MsgBoxComprar
    global MsgBoxEmptyCart

    productos = ft.Column(
        scroll= 'auto',
        width=335 * 0.82,
        height= 600 * 0.65,
        spacing= 5,


        controls=[

        ]
    )

    def _setDate(e):
        
        now = datetime.now()
        date = now.strftime('%d.%m.20%y')
        return date

    def _openProductDetails(e, nombre, descripcion, precio):
        nonlocal Dialog

        Dialog = _productDetails(nombre, descripcion, precio)
        page.dialog = Dialog
        Dialog.open = True
        page.update()

    def _closeProductDetails(e):
       
        if Dialog:
            if e.control.text == 'Comprar':
                try:
                    # Accediendo al Column que está dentro del Dialog
                    column = Dialog.content.controls[1]  # Obtén el Column que contiene los detalles del producto

                    # Accediendo a los controles dentro de ese Column
                    nombre = column.controls[1].controls[1].value  # nombre del producto (segundo control de la primera fila)
                    precio = column.controls[2].controls[1].value  # precio (segundo control de la segunda fila)
                    cantidad = column.controls[3].controls[1].value  # cantidad (segundo control de la tercera fila)               
                    _addProduct(e, nombre, cantidad, precio)

                except Exception as ex:
                    print(f"Error al agregar producto: {ex}")
                    _openEmptyCart(e)
        Dialog.open = False
        page.update()

    def _productList():
        database, cursor = conectarBanco()
        productos = cursor.execute(
            "SELECT nombre, descripcion, precio FROM productos"
        ).fetchall()
        
        database.commit()
        database.close()

        producto = choice(productos)
        return producto

    def _openMsgBoxComprar(e):
        global MsgBoxComprar
        if len(productos.controls) <= 0:
            _openEmptyCart(e)
        else:    
            MsgBoxComprar = _buyProduct(e)
            page.dialog = MsgBoxComprar
            MsgBoxComprar.open = True

        page.update()
    
    def _closeMsgBoxComprar(e):
        MsgBoxComprar.open = False

        page.update()

    def _openEmptyCart(e):
        global MsgBoxEmptyCart
        print(e.control)
        try:
        
            if e.control.text == 'Comprar':
                title= 'CANTIDAD'
                message= 'CANTIDAD A COMPRAR INVALIDA'
        except:        
            if e.control.icon == 'shopping_cart':
                title = 'CARRITO VACIO'
                message= "NO VAS A COMPRAR NADA? PAPI :'( "
                
        MsgBoxEmptyCart = _emptyCart(e, title, message)
        page.dialog = MsgBoxEmptyCart
        MsgBoxEmptyCart.open = True
        page.update()
    
    def _closeEmptyCart(e):

        MsgBoxEmptyCart.open = False
        page.update()

    def _totalCost(e):

        totalCost = 0

        for elemento in productos.controls:
            totalCost += float((elemento.content.controls[3].controls[1].value).replace('USD', ' ').strip())

        return totalCost

    def _emptyCart(e, title: str, message: str):
        MsgBox = ft.AlertDialog(
            title=ft.Text(
                value= title,
                size=18,
                weight='bold',
                color= ft.colors.BLUE
            ),
            content=ft.Row(
                controls=[
                    ft.Icon(
                        name=ft.icons.REMOVE_SHOPPING_CART,
                        color=ft.colors.RED,
                        size=40,
                    ),
                    ft.Text(
                        value=message,
                        size=12,
                        weight= 'bold',
                        color=ft.colors.WHITE
                    )
                ],
                spacing=10,
                width=335 * 0.85,
                height=30
            ),
            actions=[
                ft.ElevatedButton(
                    text='OK',
                    color=ft.colors.RED,
                    width=75,
                    height=40,
                    on_click= _closeEmptyCart
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        return MsgBox

    def _addProduct(e, nombre, cantidad, precio):
        
       

        productos.controls.append(
            ft.Container(
                width=335 * 0.82,
                height= 600 * 0.5 * 0.45,
                bgcolor=ft.colors.WHITE,
                border_radius=5,
                padding=ft.padding.only(left=3, right=3),

                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(
                                    value='Componente',
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                                  ft.Text(
                                    value=nombre,
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                          ft.Row(
                            controls=[
                                ft.Text(
                                    value='Precio',
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                                  ft.Text(
                                    value=precio,
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                          ft.Row(
                            controls=[
                                ft.Text(
                                    value='Cantidad',
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                                  ft.Text(
                                    value=cantidad,
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                          ft.Row(
                            controls=[
                                ft.Text(
                                    value='SubTotal',
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                                  ft.Text(
                                    value=f"USD {round(float(precio.replace('USD', '').strip()) * float(cantidad), 2)}",
                                    size=15,
                                    weight='bold',
                                    color=ft.colors.BLACK
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                    ]
                )
            )
        )

        page.update()

    def _buyProduct(e):
        date = _setDate(e)
        total = _totalCost(e)
        
        MsgBox = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Text(
                        value='Factura',
                        size=20,
                        weight='bold',
                        color=ft.colors.WHITE
                    ),
                    ft.Text(
                        value='   ',  # Espacio en blanco
                        size=20
                    ),
                    ft.Text(
                        value=date,
                        size=20,
                        weight='bold',
                        color=ft.colors.WHITE
                    )
                ]
            ),
            content=ft.Column(
                controls=[
                    productos,
                    ft.Row(
                        controls=[
                            ft.Text(
                                value='Total a Pagar',
                                size=15,
                                weight='bold',
                                color=ft.colors.WHITE
                            ),
                            ft.Text(
                                value=f'USD {total}',
                                size=15,
                                weight='bold',
                                color=ft.colors.WHITE
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    )
                ],
                width=355 * 0.65,
                height=600 * 0.70
            ),
            actions=[
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text='Pagar',
                            width=110,
                            height=30,
                            color=ft.colors.BLUE,
                            bgcolor=ft.colors.WHITE
                        ),
                        ft.ElevatedButton(
                            text='Cancelar',
                            width=110,
                            height=30,
                            color=ft.colors.RED,
                            bgcolor=ft.colors.WHITE,
                            on_click=_closeMsgBoxComprar
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                )
            ]
        )

        return MsgBox

    def _productDetails(nombre, descripcion, precio):
        return ft.AlertDialog(
            title=ft.Text(
                value='Detalles del Pedido',
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.WHITE
            ),
            content=ft.Column(
                controls=[
                    ft.Container(
                        width=250,
                        height=600 * 0.98 * 0.4,
                        image_src=f'assets/img/{nombre}'
                    ),
                    ft.Column(
                        controls=[
                            ft.Text(
                                value=descripcion,
                                size=16,
                                weight='bold',
                                color=ft.colors.WHITE,
                                text_align=ft.TextAlign.JUSTIFY
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value='Producto', size=13, weight='bold'),
                                    ft.Text(value=nombre.replace('.png', ' ').capitalize(), size=13, weight='bold')
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value='Precio', size=13, weight='bold'),
                                    ft.Text(value=f'USD {round(float(precio), 2)}', size=13, weight='bold')
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            ft.Row(
                                controls=[
                                    ft.Text(value='Cantidad', size=13, weight='bold'),
                                    ft.TextField(
                                        hint_text="cant",
                                        value='1',
                                        height=30,
                                        width=80,
                                        text_align=ft.TextAlign.END,
                                        multiline=False,
                                        autofocus= True,
                                        text_vertical_align=1,
                                        keyboard_type=ft.KeyboardType.NUMBER
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            )
                        ]
                    )
                ],
                width=250,
                height=600 * 0.65
            ),
            actions=[
                ft.ElevatedButton(
                    text="Comprar",
                    color=ft.colors.BLUE,
                    bgcolor=ft.colors.WHITE,
                    height=32,
                    width=120,
                    on_click=_closeProductDetails
                ),
                ft.ElevatedButton(
                    text="Cancelar",
                    color=ft.colors.RED,
                    bgcolor=ft.colors.WHITE,
                    height=32,
                    width=120,
                    on_click=_closeProductDetails
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

    def _topContainer():
        nombre, descripcion, precio = _productList()
        return ft.Row(
            controls=[
                ft.Container(
                    width=335 * 0.32,
                    height=600 * 0.24,
                    bgcolor=ft.colors.BLUE_GREY_200,
                    border_radius=20,
                    image_src=f'assets/img/{nombre}',
                    image_fit=ft.ImageFit.FIT_HEIGHT,
                    on_click=lambda e, nombre=nombre, descripcion=descripcion, precio=precio: _openProductDetails(e, nombre, descripcion, precio)
                )
            ]
        )

    def conectarBanco():
        database = sq.connect('assets/database/productos.db')
        cursor = database.cursor()
        return database, cursor

    def _bottomContainer():
        nombre, descripcion, precio = _productList()
        return ft.Container(
            width=335 * 0.45,
            height=600 * 0.25,
            bgcolor=ft.colors.WHITE,
            border_radius=20,
            image_src=f'assets/img/{nombre}',
            image_fit=ft.ImageFit.FIT_HEIGHT
        )

    def _top():
        return ft.Container(
            bgcolor=ft.colors.BLACK38,
            border_radius=20,
            width=335,
            height=600 * 0.35,
            padding=ft.padding.only(top=5, left=8, right=8),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(value='IMPERDIBLES', size=20, weight='bold', color=ft.colors.WHITE),
                            ft.Row(
                                controls=[
                                    ft.Stack(
                                        controls=[
                                            ft.IconButton(
                                                icon=ft.icons.SHOPPING_CART,
                                                icon_size=25,
                                                icon_color=ft.colors.WHITE,
                                                on_click= _openMsgBoxComprar
                                            ),
                                            ft.Container(
                                                width=40,
                                                height=20,
                                                alignment=ft.alignment.center,
                                                content=ft.Text(
                                                    value='9+',
                                                    size=13,
                                                    color=ft.colors.BLUE,
                                                    weight='bold'
                                                )
                                            )
                                        ]
                                    ),
                                    ft.Text(
                                        value="GAMER'S PARADISE",
                                        size=10,
                                        weight='bold',
                                        color=ft.colors.WHITE,
                                        italic=True
                                    )
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    ft.Row(
                        controls=[_topContainer() for _ in range(5)],
                        spacing=5,
                        scroll='auto'
                    )
                ]
            )
        )

    def _bottom():
        return ft.Container(
            width=335,
            height=600 * 0.98,
            padding=ft.padding.only(top=600 * 0.35, left=8, right=8),
            border_radius=20,
            bgcolor=ft.colors.BLACK,
            content=ft.Column(
                controls=[
                    ft.Tabs(
                        selected_index=0,
                        tabs=[
                            ft.Tab(
                                text='Especiales de hoy',
                                content=ft.Container(
                                    padding=ft.padding.only(top=10),
                                    content=ft.Row(
                                        controls=[_bottomContainer() for _ in range(4)],
                                        wrap=True
                                    )
                                )
                            ),
                             ft.Tab(
                                text='Más buscados',
                                content=ft.Container(
                                    padding=ft.padding.only(top=10),
                                    content=ft.Row(
                                        controls=[_bottomContainer() for _ in range(4)],
                                        wrap=True
                                    )
                                )
                            ),
                             ft.Tab(
                                text='Ofertas',
                                content=ft.Container(
                                    padding=ft.padding.only(top=10),
                                    content=ft.Row(
                                        controls=[_bottomContainer() for _ in range(4)],
                                        wrap=True
                                    )
                                )
                            ),
                             ft.Tab(
                                text='Más',
                                content=ft.Container(
                                    padding=ft.padding.only(top=10),
                                    content=ft.Row(
                                        controls=[_bottomContainer() for _ in range(4)],
                                        wrap=True
                                    )
                                )
                            ),
                            
                        ]
                    )
                ]
            )
        )

    Main = ft.Container(
        width=350,
        height=620,
        bgcolor=ft.colors.BLACK,
        border_radius=20,
        content=ft.Column(
            controls=[
                ft.Container(
                    width=335,
                    height=600,
                    bgcolor=ft.colors.BLACK,
                    border_radius=20,
                    content=ft.Stack(
                        controls=[_bottom(), _top()]
                    )
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    page.add(Main)

if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
