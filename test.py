from docxtpl import DocxTemplate, RichText, InlineImage
import tempfile
import base64
import os
from main import replaceBase64Image
doc = DocxTemplate("template.docx")

# sample data
sampleData = {
    "author": {
        "title": "Solution Architect",
        "name": "Anthony Nguyen"
    },
    "customer": {
        "title": "Product Owner",
        "name": "John Charles"
    },
    "project": {
        "name": "SUPERCOOLA POS"
    },
    "title": "SUPERCOOLA POS Specification Review",
    "parties": [
        {
            "name": "John Charles",
            "company": "SUPERCOOLA",
            "role": "Product Owner",
            "contact": {
                "mobile": "+61 413 725 625",
                "email": "jc@super.com"
            }
        },
        {
            "name": "Anthony Nguyen",
            "company": "SSW",
            "role": "Project Manager",
            "contact": {
                "mobile": "+61 413 725 625",
                "email": "anguyen@ssw.com.au"
            }
        },
        {
            "name": "Michael Smedley",
            "company": "SSW",
            "role": "Scrum Master",
            "contact": {
                "mobile": "+61 413 725 625",
                "email": "ms@ssw.com.au"
            }
        }
    ],
    "img_design": "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",
    "img_detaileddesign": "iVBORw0KGgoAAAANSUhEUgAAASsAAACoCAMAAACPKThEAAAA/1BMVEX///8Ab7n///3///v//v////oAcLgAbbkAcLoAb71hlcz8//8Abbj///gAarff6vMAarYAZ7YAbL07g78AcL0AZ7kAZrIAcbb7//wAZLL19fv///UAa733//4AbLQAZbIAZboqesHo8vjw9vcAYrQAcrQAaMGWud3D1+kAY6u1zeYAaq251erY5PIAXrVvoM6owuEAVK+HrtNklMQqf8Gqy+DV6PqBo9Opv9vg8fm41N/f5vZBgLU/jMNunsWLttq8yu4gb6jD0+/S2+1Ii7adt95ei7x2mcN5qsuYweNdj8pnl8tjn8zS6/ehyOa3y96EsN6MqcuNttBjmb89gMTQh31PAAAUdElEQVR4nO1cAXvaOLa1JVm2ItvYxmADxgEDgUAIWULapgnJTtPOa9Imzcz2//+WdyVDmhIn0Ldt0n2r830zXwGhSIerq3OvrqxpCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoK/0VACD3+IcnI/Vea1iHft+7UxevVHoj2wxCjuNfNtx6eGN2vB+FEQzH8hxHiHKEYkTpB8OphU3zwj6mGm4uBExKXuofN+F7DzJt1oC+88hcIwQQ/9Rs8HFSMMCZcMgPfhBcGkr8jj2MYL45/qLefBIQdByNswJAMjGPDwTA0bDiIFBnDUWV33FiaEkfOq653cH/Q2Whnghp85auiq+z1Zfwj44IBADFZ6WL4pt+fTm9vp/3hYFzqCOYIgR/1x6b5U0D48dsB4GI8Pjk5GY/Fv9++fSUM7GFjlEXJaXO5DGAu2jyJSvdbnCW1c231q6Lh1+3RPzcek/gL2aB/WA4Tv7VTAfi+l7S6btg+nfT3Ss2XWYo4+8Ov7NZ813dd2/Oq277fdavVMdjaw8ZIOzd3+5gTYohXhBvvquahBgtj2durWuS+c9D3TMO/L3YDbwIN10wRjJpw+Msnb8ojP3HTlApElDIW6hbVTcZc33d789f94buLuvGkc/3pwMe7OzsssXUA/M+EYSWJvz3ApGDJEFRKrWrmIG35IZ+x2hG6a4u0su6Oxo5wLPe/ZvwZmN4WMtZwxQG4wYfvRy3TtG1BELXsgAVhFFHgiuo5bNMFynbTEjKelSvj+ujD5166GAX8kOmf04NBsSeOHe2sGhwCU0uPhN60dP8Y3dkVOmrpSbmDv1+HxnUrtO0yN9Z4GYyx0zyY+QGjtm7ptlcV68+zU7D3BN7s6d9g6WF3T3Oe029x4jgIZ3N7MQQ22pODhp3rYeM6csYe2/7CneUCJVkYmeU770Hijhex1mHTuc8VwpMk1PVZZ93MYFvYK28HAbOpafru7PD2ABy6wGB4MD2cJb6b2xUwZVm2P0DPypUATH3gwx+HUdDkf+QerZEiu4INSNvyaLseLw3J0W5Ts3rpgCwQowaH9NFNWbeP43uTQCXbhM5ppj2xFaIm7CfZpJXQlIXg0+dvTjr5B3f/65SGZ1HLt3pRGkF31C0VeopfCk5Q06a28Aa0crDGXQ781J+iuzWISya1R7AVSHJx0yj5YRh5g8a9r6CJK/qunmjx46qUOxoazLyIRqEebE9OuNN42MjROoOtbsJC6bvc7Pm5Ej9bzwqk53TfPb0dY1RmljtetgHJuuXZ4bxpNCVXHGtzZsFKPrn3nczUwQ702uAprmDN34xMFsKmV5uPQUTx5sNGIKvg19nqhoHgKhQS98cn+2/BcTStbCViPlZ1/LRdIW3YsoP5cs5GEw9avWT70skFKPzvS1UPaHLa+fadfhVsRdf9ISpygsuO0d/7NqU2c3vgspHQxA8bxZiLDWZvxGCotgWyxfjx6f7bOGW6tCt//PQSRJxE4ah1g+OlR8Nl0wq8El44KNRpp9CT/xmRpcs6S/KuQZkVdw7REsH9lm2ZzPLn2XodkM0Cl7LyppP7ybjKubLdNVxpxOm3IquXOXe6YdiKbO/KWK4GNN0Ru0T1w51COPflLuveao/pK24YB2k4Sijb/YyMtaE2QqURo8Fso5n9fCy5WmdXGsGdKqWVz/fCjJ4VBdWD5StUCuTGXhksG/S7TPTtHhbvrsJY8Z6nJz3acw+bDbJWB5Cmc+nT5OsmE/sF2HJNyZW3hisC1vK6Mgr8Ab4zpH6rp0fVkpabDUdXoGytlFZAT0lyhj6T0q0cr0bVyx6cLApYLwjc046ImdcNlmDUiazgpdbglit/exPihrVDLfk6DcrNZbu406V25J1q+QbOjaFPLZf1rNOmIbMVIN6EqdkWfmQfROh9ItgM0uuNYhbYJbVPHrvacG4/G1tezpW+AVf4rGXplfO7l+gsAaPsXuYxIInjNvASpMz/7EhyStU8KnA7j3SNh760au9g87TgZc19Ya50sKu1bfHADnTmLpMxHF/XglC33Ffiq4Q46Lymh6HNwu6l3B0zGsq+u6UiHQBojlgkAvdZcyOzEkMwLiovzZVpb2BXBp8Hlu4f8lxUkRgdmp4VpvMYFocQ8FklELqBJuleA1xWhwYiNg9r74rUEGriD7Co9TBKh86mOhyhsbvz549N8afhHldr23LnqCV0+NCRsQ7sSoNtRmG/v4T9Xn59KxGyQadu79ghWucrE4sw3B4WyQGEOyl8TEOXcmdzHR7Pa3ubT++n4ke4ihvNNsyORR258Rkcx6dBZDNqX+dq0xh0Q8EOpTvzJkiAK1MwZ/p/F7gjMOPzHUlsZeo4m+twp9N5iTyywI9wRZrajS8mN2mImM0hBN340U6P+XOS73R8lsqsRY9Vz0BEHHqib+Z+LNIMvN4WKzSIdo+B6I3tCtq+1JHORlyJ0xXY2kBZ1V1bZ3T/2llkizttuZH5fSnWidH3WJ4PM/ePHO21XJKhd+UUdOq8k21fTob/MDbjqjF+gxyOwU1Nk5TRdKaJV0LCTyuCDqt2IujgTn1BlU4tEKnTSp6jnhWsMIQm0uos//zhh78nNuNKu9wXLgmkdbar22nYutSkYSFSklno0C0Lu+LIee0uuGKVKbqpyKyvpRfkGVBmCb0ANA9+3ex+LjbiKjb+8sAlIbEKJ4kFUiA9XrprYR1mGFU/iGMdgi9Smgc2aXeA9/Ylb2GtSD8NWj25Bmsb5Bd+D2zEFTcmXncoBSW67so8y7/kSSkEv69q1Ib4m/olgsCtNeepzMSwENzQdUvmXFm3qPOp/FCnbfR/OMp/EWzEFUJbSY/JkgViXAlrsCp70gdxRztldhhaujvniDcdfNMNxbGL1b3By8xDWClaZvM8IWtvPZEI/L2wEVe4Xg5C/0z8k6C3tdxfZ/IlxsMRS60gjCp9jYOK6ES5ufRwrGW5RzJbXx72yS0ms6bux/V5q98Em9lVp+2aVu0VxDYcxWXPtiLX/xvDKhTFBz3bgtgbuhg7ItKZenbE7O0bp4nrbUlb6P/9oILGOOlKiS+ypv/PuEpsy/ZPY9CBsXPjB5EV6KNXjTzdeenboZRRc44Jwte+TVkw62B49VXsktT0blc7JMY7P+fKPUAvpcN/FJtxVWqJpdTuIPBJTtYLKA1FerIp1Daup6HgCqLqSwQE4XlgW7VLcQQts38QHQZbKx3Chnlwx9V/jl25m8Q4b1u6TfWyWIKYa1N3ZAURbR1pwiJiMpUJOz1itWuRgfjSYmHU0QRvW5Kr4EEmE7g6X3BVPXD+YzSDGy5zfY83cj74oWV5c5RHfVkgz19Nvy7tKj7xFmLdLmui5K2np/38i1M/F6Z0pUNDMyYL0Vo7wE+vQULgJ+LNWJTREVl2xOFvwLvxc3O8EVd46pq65X5CMgZGQo/KtfXZIdJGPi3mzap9CKi1jxXaESEP0fo5V9F2faVDcseVf7AmbOZxA1azswwpDQOjhgNaz3j2Er+NuEIT2wauXjvSmSM0rgmu7MAXuokTZ1DN5x0G6Ri2uNL+rVT13BkKrkwzapVWOgR+F8bo9tdoUYTq/cnkdjqdnvcPAB8+TG9vb88+DuLnPnve8sINfPuVaVuW+0EcxcvM0xw0gkUp/QrkcYdrX225KvXIvCJajPtZnHM1EAFhyKLWBfru2EueMeRcBdM1vh1rN/uB61crvl9JfH+76rqplyatUfO594TNYpyvgW7r/pv8nA9E5l7XpHkuBstlOYQgUViaHnU/4LuqLGSMZfBMo+13DrmfcyeGtlyDwafG0/4K4cFurdsNTGoukxhm4LX25/y5z+k34wrEJQt3l5EKN3gZZIPcx0oy8xaHMmKGPZUmpTsdjnDJzRlMD74//iOx9nHJVXmd28FGlp3sTUe6tazvS98fvMp4/Ny1MhtxlaU2Ddnuq7zenMBMj2q6pKryWSpJ1HcDudpCas7vqki1OA9yQtv+S/tOcYJpLty+zkbZ0/ZBkGM0QFcclxfs6t6hhhtNvv6c+idjI64uqnkmYcEVyKpmlKsjs3aEmghrHU9m9SzbjvaHyy2La/WefNt0D78rJNViA32p5WuKdgdFWdNvEH8OAk1sHLmLIsTq20aT4EfOsn8hNuLqHXAVRSz79g5IScmNxUYdLNzYJFn86NHOX3dFWkQr59Mz598HMrBHjH0q+aaVy832M3K94Mp2S87zE6VtyNVRlVnUpPdEEs6oHDhllTNxqQGPuwuuwE7ucZWf5OjmbKVuHmmZx3qy8sucbzZSVLIXdmV21hU2/xpsxNXfHkQtSfveO818H7Mi3apegzrE6GoxEXt+V7wASnsrVwa2nn1XNw9WRr4yUXmmh1FtRag+ApQt1r0eak7zubWVwEZcfQpoL7BO77+FS76pS92QlMGdGPxiP6AQJab28E4vEQyh48Idj9FqHnm6I3PILKocwSa5gZ+u5+e0gdV7oQByI67KoQ1c3U8WYII+CX0qBr97iQl2+Myy0jBg5eZd0RHslweL3c4HrlY6HbZkrs+kyXz9xQqBRTaM6e31bX8JNuKqDb9+kE7uvYM4HtR0czH4Y3kbYBsiRLY7/HadAETpcMnV2we3dTJPfj+0wu61szlXOqO/LVdiij5lNLDvJ+yIQ9BXPxKLKLDtiTioyNpWqpunHeNbYXcs6uclKm8e1PYZV3J9htaoMsGbFMrU27ku+X3tCjlaBntcqLuXK58MWz0hQMHtdweYc21aSaPWwf0W3CktslT+7YN7JujNzsJX273MWa8B0IKr6MUOqjewKyT0ALOqw9VPejI1w1hEZ/WYOCch/OT8/gbFnczVpcB3J6tXs5CR0XApxF9vcGdkydXLHerfq+srbsA1NKhZVkB3363s0+iym+sExtwpJgSdBZUD416QhpoGYYvSvvnD24Xax6V+ZfZ4/UgXXIU0eLna2jCv2X6MKzCYI1+3WK96sdIibtaiBVds99jhxkUl7XzHJ3jsBRvmrL7aP3eOU9My5Tr0rsTh4pp1eGdXL1hbK9Wz/yhX3DmHhQRcnawaBr5dRrPWqCyuKb/vo9XYbqZLNuz2g5N47qBbN8+yWFbtCJTGmnWYc2W/HFdXuV09fm8Ca0ik5UJaXbUM3CjVFlxF0c4R4o2s7qzmSa7A08kmq78FQrFzPGLUlDIgHB0b2tMx9O/A1cKuHuUKAmB5Uqqv3u4lTXS4MCwT1mjHgNC/uXq1fGLLmlG9dr1aYiYu/J6npjxaDK2k3FxD1W/AVaDnd+LGj0RYoJZmoqyT9Qrq6cbVJFokK91bXJQ4P/fkGqTbw4L+MZmzIJDVbunOISfkiftgS9/+glyV77h6xK4gVBuJMRaPcJ5Ei2UY7l4XBXVH+T5L/cui/nnJEze/hWH3gsOm4xTch1viN+CKSf1jF5ayCBAsy9GsYKuACvSlZi/JSv5VJJLeVQPRgCbTAq54Ax3tRjRXtD3/z+zJI50X52oWSq7Y41w5Y+mUQE0WcEXKwR1XkyKuLjzpD2nrrKBvDD7qdjcKYAgms9LKKTgCJJ4dUVg++6JciRKgdioTK8z752ONUB7T+edFE8A3O0uu/EGRVZT8PDHvlx+568XPdiJYpsLFR0n1BjZSpBUpLYTrbfqCdgVSOpV5FT30Dh5pw9FRztVNwVwR6liLHJ97ZfAC992p5ec9btR5+KHsgp+1WBJK47OYv1UyMC7aERF6Wa4w7qR6nlkxPzzSBuX5urB7VFB3QBBaZvP8gYEKDqGQK7NUVlh9ZJETA093w/xiHk3txJt2NKfQb9VzJfgyXBEnHnswDTEA90wzCh+mgdAnQSbtDh3xFKMHnx5X5T5nlsECV8gkIossk+ogOdIz8EMQNa6yII5o9qIgYpYZQrBEmb89kRfMuXwCgrjpg8XXEBruysiVmi8RD/JmY2+RX9Jbc8ybRU8B4s223NMrNwa43JWjPHGSNbHB3UQ7BZdkBFdoLtVmFIS7Jw7nxRe+cOnQD3r6Iu3A3NH7N6W4IXMcCOVPxGqWplVpV1YavgRXDmp8XkZ0SVpChWKyMZAl+6b3t9MgD7Q34s6rXVH42S7wMYKYxtyTdssCVs4aTnEdEDf4UbkVLIaigz51q7NPbwalrC6QjYcfy5WUhUK89Bg7/BmT/1GQAV0+I0VPy6WsYKfD45ks67BYtPfwvEU8zUt7n0bW/l7B4TFwRQY2EzOExZWyPy5LxQ4eNTXc6Uf5VXKdRtQDNZ/6vmdZ7Xaben4lSUzdomI5Rzv7z355AA8+XX31AtsSj04Se5Xn0tnV1qSznDSPyeXWVRnYzDMFpt/+uvWp9ODIBe11e3ZhkToelttu4NrQv5yoXfXa5a2tSX21LZLpm/qbWatCrRAUnxVFqXTkJsA2dRqKjKIltM3+/NmpQtofO76Q44yZMB9mstCybNv+x5tlCxIPamnVDAEeDBhCEduzax/RatmT4ZSDVuENQV6uQMit2wH8AZPZJvTlmq63f9MolloOHpy1ui5LYDQMYp9czliWoC6ioZ5WutFk/PzP3UH8dhRV9TTq9WazWa9HaZrarjeKrpePc0GN+rxiQ+gbyRYwWjPw3D1jdScj6Ga/R4qKPp1BuUdhEZXL5dksaoN5pVEauOXSI5FME7Y8PvhYjvydip1LmQUCZpotb3b2liCj0Kv+WhhO6eREOE9Z1kjAg2bijc6dgXAunpt3clKvc2GG0EB87MTGaioZO7d7pKjAh2jO8nwGNjPORRel0vIZBQXtFwItG/Qn83Joum5NPobODNvlw+mgJCQICI8XOZ//rQG/03gsHoI1eDUu1bXNL2P+10E8nJKjb9AKH0+pIEGEwhePPkXyWZkP9b7CEthAQuPnZYQoJhs8QEVBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB4T8B/wvSK5cHfxSzDQAAAABJRU5ErkJggg==",
    "ui_areas": ["Login and Sign up page", "Home page", "Report", "Checkout"],
    "has_more": True,
    "outscope": ["Payment gateway", "Support after deployment"],
    "total": "230 h",
    "std": "$33,400",
    "pre": "$30,400",
    "tasks": [
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Login screen",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800",
            "bg": "42f557",
            "mvp": "Y"
        },
        {
            "name": "Sign up screen",
            "est": "8 h",
            "std": "$2,100",
            "pre": "$1,800"
        },
        {
            "name": "Google Sign In",
            "est": "16 h",
            "std": "$4,100",
            "pre": "$3,800"
        }
    ]
}

# replace base64 image with temp file
tempFiles = replaceBase64Image(doc, sampleData)

# render
doc.render(sampleData)
doc.save("output.docx")

# Delete tmp file
[os.unlink(f) for f in tempFiles]
