import flet as ft
from time import sleep
import re

def main(page: ft.Page):
    page.window_always_on_top=True
    page.window_height=640
    page.window_width=390
    page.window_max_height=640
    page.window_max_width=390
    page.window_resizable=False
    page.window_center = True
    page.title="Calculator"
    page.padding=0
    
    dict_buttons = [
        ("AC", ft.colors.BLUE_GREY_300, ft.colors.BLACK),
        ("±", ft.colors.BLUE_GREY_300, ft.colors.BLACK),
        ("%", ft.colors.BLUE_GREY_300, ft.colors.BLACK),
        ("/", ft.colors.ORANGE_300, ft.colors.WHITE),
        ("7", ft.colors.GREY_800, ft.colors.WHITE),
        ("8", ft.colors.GREY_800, ft.colors.WHITE),
        ("9", ft.colors.GREY_800, ft.colors.WHITE),
        ("*", ft.colors.ORANGE_300, ft.colors.WHITE),
        ("4", ft.colors.GREY_800, ft.colors.WHITE),
        ("5", ft.colors.GREY_800, ft.colors.WHITE),
        ("6", ft.colors.GREY_800, ft.colors.WHITE),
        ("-", ft.colors.ORANGE_300, ft.colors.WHITE),
        ("1", ft.colors.GREY_800, ft.colors.WHITE),
        ("2", ft.colors.GREY_800, ft.colors.WHITE),
        ("3", ft.colors.GREY_800, ft.colors.WHITE),
        ("+", ft.colors.ORANGE_300, ft.colors.WHITE),
        ("( )", ft.colors.BLUE_GREY_300, ft.colors.BLACK),
        ("0", ft.colors.GREY_800, ft.colors.WHITE),
        (".", ft.colors.GREY_800, ft.colors.WHITE),
        ("=", ft.colors.ORANGE_300, ft.colors.WHITE),
    ]
    
    def operation(expression):
        if len(expression) > 1:
            if expression[-1] == "(":
                expression = expression[:-1]
            if expression.count("(") > expression.count(")"):
                diff_parenth = expression.count("(") - expression.count(")")
                expression += ")" * diff_parenth
        
        try:
            return str(eval(expression.replace("%", "/100")))
        except:
            return ""

    # FUNCTIONS
    def calculation(e):
        pattern = r'(\(-\d+\.\d+|\d+\.\d+|\d+|[*\/\-\+]|\(-\d+)'
        
        value = e.control.content.value
        
        value_split = re.findall(pattern, type_area.value)
        
        if value == "AC":
            type_area.value = ""
        
        elif value == "±":
            if type_area.value == "":
                type_area.value += "(-"
            elif type_area.value == "(-":
                type_area.value = ""
            
            elif type_area.value[-3:] == "*(-":
                type_area.value = type_area.value[:-3]

            elif type_area.value[-2:] == "(-":
                type_area.value = type_area.value[:-2]
            
            elif type_area.value[-1] in [")","%"]:
                type_area.value += "*(-"
            elif type_area.value[-1] in ["*","/","+","-","("]:
                type_area.value += "(-"         
            
            elif value_split[-1][:2] == "(-":
                value_split[-1] = value_split[-1].replace("(-", "")
                type_area.value = "".join(value_split)

            elif value_split[-1].replace("-", "").replace(".", "").replace("(", "").replace(")", "").isnumeric():
                value_split.insert(-1, "(-")
                type_area.value = "".join(value_split)
        
        elif value == "( )":
            if type_area.value == "":
                type_area.value += "("
            elif type_area.value == "(":
                type_area.value = ""

            elif type_area.value[-1] in ["*", "/", "-", "+"]:
                type_area.value += "("
            elif type_area.value[-1:] == "(":
                type_area.value = type_area.value[:-1]

            elif type_area.value.count("(") > type_area.value.count(")"):
                type_area.value += ")"
            

            elif value_split[-1].replace("-", "").replace(".", "").replace("(", "").replace(")", "").isnumeric() or type_area.value[-1] in [")", "%"]:
                type_area.value += "*("
            elif type_area.value[-2:] == "*(":
                type_area.value = type_area.value[:-2]


        elif value in "%/*-+=" and type_area.value == "":
            type_area.value = "Invalid operation"
            type_area.update()
            sleep(0.5)
            type_area.value = ""
            temp_result.value = ""

        elif value == "." and "." in type_area.value:
            pass
        
        elif value == "." and (type_area.value == "" or type_area.value[-1] in "+-*/"):
            type_area.value += "0."
        
        elif value[-1].replace("-", "").replace(".", "").replace("(", "").replace(")", "").isnumeric():
             type_area.value += value
        
        elif value in ["%", "/", "*", "-", "+"]:
            if value in ["*", "-", "/", "+"] and type_area.value[-1] in ["*", "-", "/", "+"]:
                type_area.value = type_area.value[:-1] + value
            elif value == "%" and type_area.value[-1] in "0123456789)":
                type_area.value += "%"
            elif value == "%" and type_area.value[-1] in ["*", "-", "/", "+"]:
                pass
            else:
                type_area.value += value



        elif value == "=":
            type_area.value = operation(type_area.value)
            temp_result.value = ""
        
        if value != "=":
            temp_result.value = operation(type_area.value)
        
        
        type_area.update()
        temp_result.update()
        
        

    
    
    
    # TYPE AREA
    type_area = ft.TextField(
        text_size=30,
        color=ft.colors.BLACK,
        text_align=ft.TextAlign.RIGHT,
        border=ft.InputBorder.NONE,
        content_padding=ft.padding.all(15),
        #bgcolor="BLACK"
    )


    # TEMP RESULT
    temp_result = ft.TextField(
        text_size=20,
        color=ft.colors.BLACK,
        text_align=ft.TextAlign.RIGHT,
        border=ft.InputBorder.NONE,
        content_padding=ft.padding.all(15)
    )

    # BUTTONS
    buttons = ft.Row(
        controls=[
            ft.Container(
                bgcolor=item[1],
                height=80,
                width=80,
                border_radius=100,
                margin=ft.margin.all(10),
                on_click=calculation,
                content=ft.Text(value=item[0], size=25, text_align=ft.TextAlign.CENTER, color=item[2]),
                alignment=ft.alignment.center
            ) for item in dict_buttons
        ],
        spacing=-10,
        run_spacing=-10,
        wrap=True,
        alignment=ft.MainAxisAlignment.END
    )


    layout = ft.Container(
        content=ft.Column(
            controls=[
                type_area,
                temp_result,
                buttons
            ]
        ),
        image_src="bck.jpg",
        image_opacity=0.5,
        #bgcolor=ft.colors.BLACK,
        expand=True,
        image_fit=ft.ImageFit.FIT_HEIGHT,
        height=640,
        width=390,
    )


    page.add(layout)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")