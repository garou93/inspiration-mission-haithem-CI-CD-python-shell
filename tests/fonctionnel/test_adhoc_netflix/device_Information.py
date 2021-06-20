import sc_stbt
import stbts
import stbt

menu=sc_stbt.menu()

def goto_information():

    if stbts.match_any_text(text=['watching', 'regarde', 'quiere'],
                            region=stbt.Region(x=356, y=41, width=278, height=74)).match:
        sc_stbt.press('KEY_OK')
        sc_stbt.wait(5)
    # back to movie netflix menu
    if sc_stbt.back_to_netflix_movie_menu():
        sc_stbt.debug("NETFLIX MOVIE MENU FOUND")
    else:
        sc_stbt.debug("NETFLIX MOVIE MENU NOT FOUND")
    # goto get help menu in netflix
    sc_stbt.goto_settings_menu()

    menu.is_menu(press=['KEY_DOWN'],
                      text="Get help",

                      timeout_is_menu=3,
                      region_text=stbt.Region(x=369, y=72, width=81, height=32),
                      timeout=20)

    menu.is_menu(press=['KEY_OK'],
                      text="Get help",
                      timeout_is_menu=3,
                      region_text=stbt.Region(x=69, y=59, width=111, height=43),
                      timeout=20)

    menu.is_menu(press=['KEY_DOWN'],
                      text="ESN",
                      timeout_is_menu=3,
                      region_text=stbt.Region(x=365, y=71, width=61, height=28),
                      timeout=20)

def get_esn(esn=None):
    """
    get the esn from the technical information
    :return: the middleware version as string
    """
    if esn is None:
        esn_value = sc_stbt.is_text(mode=stbt.OcrMode.SINGLE_LINE,
                                    region=stbt.Region(x=369, y=96, width=312, height=33))
        sc_stbt.write_csv_file(file_name="esn_information", rows=esn_value)
    else:
        if menu.is_menu_ocr(perf=False,
                            text=esn,
                            region_text=stbt.Region(x=369, y=96, width=312, height=33),
                            mode=stbt.OcrMode.SINGLE_LINE):
            sc_stbt.debug("esn is found")
        else:
            assert False, "Esn not found"

def get_device_model(device_model=None):
    """
    get the esn from the technical information
    :return: the middleware version as string
    """
    if device_model is None:
        device_model_value = sc_stbt.is_text(mode=stbt.OcrMode.SINGLE_LINE,
                                    region=stbt.Region(x=364, y=343, width=443, height=31))
        sc_stbt.write_csv_file(file_name="device_model", rows=device_model_value)
    else:
        if menu.is_menu_ocr(perf=False,
                            text=device_model,
                            region_text=stbt.Region(x=364, y=343, width=443, height=31),
                            mode=stbt.OcrMode.SINGLE_LINE):
            sc_stbt.debug("device model is found")
        else:
            assert False, "device model not found"

def get_software_version(software=None):
    """
    get the esn from the technical information
    :return: the middleware version as string
    """
    if software is None:
        software_value = sc_stbt.is_text(mode=stbt.OcrMode.SINGLE_LINE,
                                    region=stbt.Region(x=371, y=147, width=529, height=44))
        sc_stbt.write_csv_file(file_name="software_version", rows=software_value)
    else:
        if menu.is_menu_ocr(perf=False,
                            text=software,
                            region_text=stbt.Region(x=371, y=147, width=529, height=44),
                            mode=stbt.OcrMode.SINGLE_LINE):
            sc_stbt.debug("software is found")
        else:
            assert False, "software not found"


def get_ui_build(ui_build=None):
    """
    get the esn from the technical information
    :return: the middleware version as string
    """
    if ui_build is None:

        ui_build = sc_stbt.is_text(mode=stbt.OcrMode.SINGLE_LINE,
                                    region=stbt.Region(x=365, y=394, width=465, height=38))
        sc_stbt.write_csv_file(file_name="UI_build", rows=ui_build)
    else:
        if menu.is_menu_ocr(perf=False,
                            text=ui_build,
                            region_text=stbt.Region(x=365, y=394, width=465, height=38),
                            mode=stbt.OcrMode.SINGLE_LINE):
            sc_stbt.debug("ui build is found")
        else:
            assert False, "ui build not found"

#################################API Call#################################################

goto_information()
get_esn(esn=None)
get_software_version(software=None)
get_device_model(device_model=None)
get_ui_build(ui_build=None)

