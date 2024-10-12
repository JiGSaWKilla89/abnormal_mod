init 1:# Styles

    style notify_item_frame:
        background Frame("gui/textbox.png", 180,8,180,8, tile=gui.frame_tile)
        padding (180,8,180,8)
    style notify_item_text:
        properties gui.text_properties("notify")
        outlines [(2, "#0009", 1, 1)]

    style file_slots_delete_button:
        hover_background None
        align (1.0,0.0)
    style file_slots_delete_button_text:
        properties gui.text_properties("slot_delete")
        bold True
        text_align 0.5

    style input_prompt:
        xalign gui.dialogue_text_xalign
        properties gui.text_properties("input_prompt")
    style input_button_text:
        properties gui.text_properties("input_button")
        text_align 0.5
    style input_button:
        properties gui.button_properties("input_button")

    style input_hint_vbox:
        xalign 0.98
        yalign 0.5
    style input_hint_button is input_button
    style input_hint_button_text is input_button_text

    style tooltip_frame:
        padding (50,10,50,10)
        xfill False
        yfill False
        align (0.5,0.5)
    style tooltip_hbox:
        align (0.5,0.5)
    style tooltip_text:
        size gui.text_size -10
        text_align 0.5
    style tooltip_button_text is gui_button_text:
        color "#FB4301"
        hover_color "#FFF"
        outlines [(2, "#0009", 1, 1)]
    style tooltip_button is gui_button
    style tooltip_vscrollbar is gui_vscrollbar:
        unscrollable "hide"
        base_bar Frame(Solid("#FB4301"), gui.vscrollbar_borders, tile=gui.scrollbar_tile)
        thumb Frame(Solid("#000"), gui.vscrollbar_borders, tile=gui.scrollbar_tile)


    style quick_button is default
    style quick_button_text is button_text
    style quick_button:
        properties gui.button_properties("quick_button")
    style quick_button_text:
        properties gui.text_properties("quick_button")

    style quick_menu_bottom_center_text is quick_menu_text
    style quick_menu_bottom_center_hbox:
        xalign 0.5
        yalign 1.0
    style quick_menu_bottom_center_button is quick_button
    style quick_menu_bottom_center_button_text is quick_button_text

    style quick_menu_top_center_text is quick_menu_text
    style quick_menu_top_center_hbox:
        xalign 0.5
        yalign 0.05
    style quick_menu_top_center_button is quick_button
    style quick_menu_top_center_button_text is quick_button_text

    style replay_unlocked_button is gui_button:
        align (1.0, 0.5)
    style replay_unlocked_button_text is gui_button_text:
        outlines [(2, "#0009", 1, 1)]
        size gui.text_size+20
        text_align 1.0
        align (0.5,0.5)
        #bold True
        #italic True
        #underline True
    style replay_unlocked_vbox:
        xsize 600
        align (0.96,0.98)

    style shortcuts_button_text is gui_button_text:
        outlines [(2, "#0009", 1, 1)]
        text_align 0.5
        size gui.text_size+15
    style shortcuts_text is shortcuts_button_text

    style splash:
        outlines [(2, "#a2a2a2", 1, 1)]
        text_align 0.5
        align (0.5,0.5)


style custom_caret:
    color gui.accent_color
    xalign 0.0
    yalign 0.5
    text_align 0.5

style custom_caret_2:
    color gui.accent_color
    size gui.text_size-10
    xalign 0.0
    yalign 0.5
    text_align 0.5


image custom_caret_2:
    Text("|", style="custom_caret_2")
    pause .5
    Text("")
    pause .5
    Text("|", style="custom_caret_2")
    pause .5
    repeat

image custom_caret:
    Text("|", style="custom_caret")
    pause .5
    Text("")
    pause .5
    Text("|", style="custom_caret")
    pause .5
    repeat