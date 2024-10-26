define default_outlines = [(2, "#0009", 1, 1)]
init 1:# Styles

    style notify_item_frame:
        background Frame(gui.textbox_location, 90,8,90,8, tile=gui.frame_tile)
        padding (180,8,180,8)
    style notify_item_text:
        properties gui.text_properties("notify")
        outlines default_outlines

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
        outlines default_outlines
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
        yalign 0.0
    style quick_menu_top_center_button is quick_button
    style quick_menu_top_center_button_text is quick_button_text

    style replay_unlocked_button is gui_button:
        align (1.0, 0.5)
    style replay_unlocked_button_text is gui_button_text:
        outlines default_outlines
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
        outlines default_outlines
        text_align 0.5
        size gui.text_size+15
    style shortcuts_text is shortcuts_button_text

    style splash:
        outlines [(2, "#a2a2a2", 1, 1)]
        text_align 0.5
        align (0.5,0.5)
        font "mod/CabinSketch-Regular.ttf"


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

#Style Overrides
style pref_label_text:
    properties gui.text_properties("pref_label")

style confirm_prompt_text:
    properties gui.text_properties("confirm_prompt")

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")

style history_name_text:
    properties gui.text_properties("history_name")

style history_text:
    properties gui.text_properties("history_text")

style history_label_text:
    properties gui.text_properties("history_label")

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")

style radio_button:
    properties gui.button_properties("radio_button")

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_button:
    properties gui.button_properties("check_button")

style check_button_text:
    properties gui.text_properties("check_button")

style slider_button:
    properties gui.button_properties("slider_button")

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style help_text:
    properties gui.text_properties("help_text")

style skip_text:
    properties gui.text_properties("skip")

style slot_name_text:
    properties gui.text_properties("slot_name")

style page_label:
    properties gui.text_properties("page_label")

style page_label_text:
    properties gui.text_properties("slot_page")

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")

style file_slots_delete_button_text:
    properties gui.text_properties("slot_delete")

style about_text:
    properties gui.text_properties("about_text")

style about_label_text:
    properties gui.text_properties("about_label")

style game_menu_label_text:
    properties gui.text_properties("game_menu_label")

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")

style navigation_button_text:
    properties gui.text_properties("navigation_button")

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")



define gui.main_menu_text_outlines = default_outlines
#define gui.title_text_outlines = default_outlines
#define gui.version_text_outlines = default_outlines
define gui.game_menu_label_text_outlines = default_outlines
define gui.history_name_text_outlines = default_outlines
define gui.history_text_text_outlines = default_outlines
define gui.history_label_text_outlines = default_outlines
define gui.navigation_button_text_outlines = default_outlines
## to your navigation text button text outlines and uncomment the ones below
#define gui.navigation_button_text_idle_outlines = default_outlines
#define gui.navigation_button_text_hover_outlines = default_outlines
#define gui.navigation_button_text_selected_outlines = default_outlines
#define gui.navigation_button_text_insensitive_outlines = default_outlines
define gui.about_label_text_outlines = default_outlines
define gui.about_text_text_outlines = default_outlines
define gui.about_music_button_text_outlines = default_outlines
#define gui.about_music_button_text_idle_outlines = default_outlines
#define gui.about_music_button_text_hover_outlines = default_outlines
#define gui.about_music_button_text_selected_outlines = default_outlines
#define gui.about_music_button_text_insensitive_outlines = default_outlines
define gui.about_music_text_outlines = default_outlines
define gui.input_prompt_text_outlines = default_outlines
define gui.input_text_outlines = default_outlines
define gui.input_hint_text_outlines = default_outlines
define gui.input_button_text_outlines = default_outlines
# to your input buttons text outlines and uncomment the ones below
#define gui.input_button_text_idle_outlines = default_outlines
#define gui.input_button_text_hover_outlines = default_outlines
define gui.choice_button_text_idle_outlines = default_outlines
define gui.choice_button_text_hover_outlines = default_outlines
define gui.choice_button_text_insensitive_outlines = default_outlines
define gui.choice_alt_button_text_idle_outlines = gui.choice_button_text_idle_outlines
define gui.choice_alt_button_text_hover_outlines = gui.choice_button_text_hover_outlines
define gui.choice_alt_button_text_insensitive_outlines = gui.choice_button_text_hover_outlines
define gui.choice_tooltip_text_outlines = default_outlines
define gui.quick_button_text_outlines = default_outlines
# to your quick menu buttons text outlines and uncomment the ones below
#define gui.quick_button_text_idle_outlines = default_outlines
#define gui.quick_button_text_hover_outlines = default_outlines
#define gui.quick_button_text_selected_outlines = default_outlines
#define gui.quick_button_text_insensitive_outlines = default_outlines
define gui.quick_menu_text_outlines = default_outlines
define gui.name_text_outlines = default_outlines
define gui.dialogue_text_outlines = default_outlines
define gui.slot_button_text_outlines = default_outlines
# to your slot text button text outlines and uncomment the ones below
#define gui.slot_button_text_idle_outlines = default_outlines
#define gui.slot_button_text_hover_outlines = default_outlines
define gui.slot_name_text_outlines = default_outlines
# to your slot name text outlines and uncomment the ones below
#define gui.slot_name_text_idle_outlines = default_outlines
#define gui.slot_name_text_hover_outlines = default_outlines
define gui.slot_delete_text_outlines = default_outlines
# to your slot delete button text outlines and uncomment the ones below
#define gui.slot_delete_text_idle_outlines = default_outlines
#define gui.slot_delete_text_hover_outlines = default_outlines
define gui.slot_page_text_outlines = default_outlines
# to your page heading button text outlines and uncomment the ones below
#define gui.slot_page_text_idle_outlines = default_outlines
#define gui.slot_page_text_hover_outlines = default_outlines
#define gui.slot_page_text_selected_outlines = default_outlines
define gui.page_button_text_outlines = default_outlines
# to your page button text outlines and uncomment the ones below
#define gui.page_button_text_idle_outlines = default_outlines
#define gui.page_button_text_hover_outlines = default_outlines
#define gui.page_button_text_selected_outlines = default_outlines
define gui.radio_button_text_outlines = default_outlines
define gui.check_button_text_outlines = default_outlines
define gui.slider_button_text_outlines = default_outlines
define gui.pref_label_text_outlines = default_outlines
define gui.help_button_text_outlines = default_outlines
# to your help text button text outlines and uncomment the ones below
#define gui.help_button_text_idle_outlines = default_outlines
#define gui.help_button_text_hover_outlines = default_outlines
#define gui.help_button_text_selected_outlines = default_outlines
define gui.help_label_text_outlines = default_outlines
define gui.help_text_text_outlines = default_outlines
define gui.confirm_button_text_outlines = default_outlines
# to your confirm buttons text outlines and uncomment the ones below
#define gui.confirm_button_text_idle_outlines = default_outlines
#define gui.confirm_button_text_hover_outlines = default_outlines
define gui.confirm_prompt_text_outlines = default_outlines
define gui.skip_text_outlines = default_outlines
define gui.notify_text_outlines = default_outlines
define gui.tooltip_text_outlines = default_outlines