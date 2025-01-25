# [Unnamed Game]

- Incremental minimal game that simulates a very simplified economy bubble

# TODO
- [x] App wide consistent theming for UI and other game objects
    - [x] One thing to do is to decide on a font and consistently use it for all UI elements
        - Here be some fonts from this [website](https://www.fontspace.com/)
            - [font1](https://www.fontspace.com/poppin-gumi-font-f121602)
            - [font2](https://www.fontspace.com/theren-regular-font-f107067)
            - [font3](https://www.fontspace.com/sheriff-bounce-font-f85031)

- [ ] Fill NewsStrip with content
    - [ ] First fill out [content.py](./gameObjects/content.py)
    - [ ] Then loop through the keys and apply the efffect tag according to category
    - [ ] Decide on how to set what news to show asw and in which class or ask gpt, claude or deepseeksongchu or wutteva da fugg da new model is

- [ ] Polish the game and make it presentable
    - [ ] If nae then prolly leave
    


## Libraries used
- pygame-ce
- pygame_gui


### pygame_gui
We use pygame_gui for drawing the buttons, the news thingy during play state and dropdown menu.

Prolly seems like overkikill at this point but making custom ui thingies will be wasteful

We are mostly using few UI elements

- [`UIButton`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_button)
    - For all pressable buttons

- [`UIDropDownMenu`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_drop_down_menu)
    - We are only using this in the `OptionsMenu` state
- [`UITextBox`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_text_box)
    - This is being used in The GameUI class in the `gameObjects` module for the `News` class

The styling docs are here
- [pygame_gui Theme Guide](https://pygame-gui.readthedocs.io/en/latest/theme_guide.html)
    - Docs are a bit sparse but we are not bitching about it, you can make sense of it if you just read and take a look at functions prototypes and the types of the parameters

    - Biggest annoyance is the declarative nature of the UI styling using json but prolly can provide a dict asw , oh well here it is the [`UIManager`](https://pygame-gui.readthedocs.io/en/latest/theme_guide.html) initialization prototype

    - Bigger annoyance is reloading themes takes a  lot of time...
