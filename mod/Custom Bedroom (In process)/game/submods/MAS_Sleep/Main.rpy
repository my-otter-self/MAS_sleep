################################################################################
## BED
################################################################################

###START: IMAGE DEFINITIONS

#Day images
image submod_background_bedroom_day = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_rain = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_overcast = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_snow = "mod_assets/location/bedroom_submod/bedroom.png"

#Night images
image submod_background_bedroom_night = "mod_assets/location/bedroom_submod/bedroom-n.png"
image submod_background_bedroom_rain_night = "mod_assets/location/bedroom_submod/bedroom-n.png"
image submod_background_bedroom_overcast_night = "mod_assets/location/bedroom_submod/bedroom-n.png"
image submod_background_bedroom_snow_night = "mod_assets/location/bedroom_submod/bedroom-n.png"

#Sunset images
image submod_background_bedroom_ss = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_rain_ss = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_overcast_ss = "mod_assets/location/bedroom_submod/bedroom.png"
image submod_background_bedroom_snow_ss = "mod_assets/location/bedroom_submod/bedroom.png"

default persistent.submod_acs_bedroom = None

init -1 python:

    submod_background_bedroom_test = MASFilterableBackground(
        # ID
        "submod_background_bedroom_test",
        "Bedroom (MAS-Sleep)",

        # mapping of filters to MASWeatherMaps
        MASFilterWeatherMap(
            day=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_bedroom_day",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_bedroom_rain",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_bedroom_overcast",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_bedroom_snow",
            }),
            night=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_bedroom_night",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_bedroom_rain_night",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_bedroom_overcast_night",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_bedroom_snow_night",
            }),
            sunset=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "submod_background_bedroom_ss",
                store.mas_weather.PRECIP_TYPE_RAIN: "submod_background_bedroom_rain_ss",
                store.mas_weather.PRECIP_TYPE_OVERCAST: "submod_background_bedroom_overcast_ss",
                store.mas_weather.PRECIP_TYPE_SNOW: "submod_background_bedroom_snow_ss",
            }),
        ),

        MASBackgroundFilterManager(
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            ),
            MASBackgroundFilterChunk(
                True,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_DAY,
                    60
                ),
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_SUNSET,
                    60,
                    30*60,
                    10,
                ),
            ),
            MASBackgroundFilterChunk(
                False,
                None,
                MASBackgroundFilterSlice.cachecreate(
                    store.mas_sprites.FLT_NIGHT,
                    60
                )
            )
        ),

        #FOR BACKGROUND PROPERTIES (DON'T TOUCH "ENTRY_PP:/EXIT_PP:)
        disable_progressive=False,
        hide_masks=False,
        hide_calendar=True,
        unlocked=True,
        entry_pp=store.mas_background._bedroom_entry,
        exit_pp=store.mas_background._bedroom_exit,
        ex_props={"skip_outro": None}
    )


init -2 python in mas_background:
    def _bedroom_entry(_old, **kwargs):
        """
        Entry programming point for bedroom background

        NOTE: ANYTHING IN THE `_old is None` CHECK WILL BE RUN **ON LOAD ONLY**
        IF IT IS IN THE CORRESPONDING 'else' BLOCK, IT WILL RUN WHEN THE BACKGROUND IS CHANGED DURING THE SESSION

        IF YOU WANT IT TO RUN IN BOTH CASES, SIMPLY PUT IT AFTER THE ELSE BLOCK
        """
        if kwargs.get("startup"):
            pass

        #COMMENT(#) IF NOT NEEDED
        else:
            if not store.mas_inEVL("bedroom_switch_dlg"):
                store.pushEvent("bedroom_switch_dlg")
            store.mas_o31HideVisuals()
            store.mas_d25HideVisuals()

        store.monika_chr.tablechair.table = "transparent"
        store.monika_chr.tablechair.chair = "transparent"
        
        if store.persistent.submod_acs_bedroom == True:
            pass
        else:
            store.monika_chr.wear_acs(store.acs_zero_white_pillow)
            store.monika_chr.wear_acs(store.acs_zero_white_blanket)

        #IF THIS IS NOT A FURNISHED SPACEROOM, COMMENT THESE TWO LINES
        if store.seen_event("mas_monika_islands"):
            store.mas_unlockEVL("mas_monika_islands", "EVE")

        #IF THIS BACKGROUND FORCES WEATHER, UNCOMMENT THESE LINES
        #store.mas_weather.temp_weather_storage = store.mas_current_weather
        #store.mas_changeWeather(store.mas_weather_def, by_user=True, set_persistent=True) #Forces to clear weather, can be changed to others as required

    def _bedroom_exit(_new, **kwargs):
        """
        Exit programming point for bedroom background
        """
        #O31
        if store.persistent._mas_o31_in_o31_mode:
            store.mas_o31ShowVisuals()
                  
        #D25
        elif store.persistent._mas_d25_deco_active:
            store.mas_d25ShowVisuals()

        #Lock islands greet to be sure
        store.mas_lockEVL("mas_monika_islands", "EVE")

        #COMMENT(#) IF NOT NEEDED
        store.monika_chr.tablechair.table = "def"
        store.monika_chr.tablechair.chair = "def"
        store.remove_acs_bedroom("pillow_selector")
        store.remove_acs_bedroom("blanket_selector")
        store.remove_acs_bedroom("objets_selector")

        if _new == store.mas_background_def or not _new == store.mas_background_def:
            store.acs_bedroom(test=False)
            store.pushEvent("return_switch_dlg")

###START: Topics
#THIS ONE RUNS ON CHANGE
label bedroom_switch_dlg:
    python:
        switch_quip = renpy.substitute(renpy.random.choice([
            "It is very cozy",
            "It is very comfortable"
        ]))

    m 1hua "[switch_quip]"

    return

###START: Topics
#THIS ONE RUNS ON CHANGE
label return_switch_dlg:
    python:
        switch_quip = renpy.substitute(renpy.random.choice([
            "No sleep?",
            "No sleep..."
        ]))

    m 1hua "[switch_quip]"

    return

init python:

    def acs_bedroom(test=None):
        if test == True:
            persistent.submod_acs_bedroom = True
        elif test == False:
            persistent.submod_acs_bedroom = False
    
    def remove_acs_bedroom(acs_type):
        images = store.mas_sprites.get_acs_of_type(acs_type)
        index = 0
        while index < len(images):
            image_name = images[index]
            monika_chr.remove_acs(image_name)
            index += 1

    ### PILLOW AND BLANKET TEST ###
    acs_zero_white_blanket = MASAccessory(
        "zero_white_blanket",
        "zero_white_blanket",
        MASPoseMap(
            default="0",
            l_default = "0"
        ),
        priority=13,
        stay_on_start=True,
        acs_type="blanket_selector",
        rec_layer=2
    )
    store.mas_sprites.init_acs(acs_zero_white_blanket)
    store.mas_selspr.init_selectable_acs(
        acs=acs_zero_white_blanket,
        display_name="Blanket Test",
        thumb="zero_white_blanket",
        group="blankets",
        select_dlg=[
            "Only Test :p"
        ]
    )

    # ###################################
    acs_zero_white_pillow = MASAccessory(
        "zero_white_pillow",
        "zero_white_pillow",
        MASPoseMap(
            default="0",
            l_default = "0"
        ),
        priority=13,
        stay_on_start=True,
        acs_type="pillow_selector",
        rec_layer=0
    )
    store.mas_sprites.init_acs(acs_zero_white_pillow)
    store.mas_selspr.init_selectable_acs(
        acs=acs_zero_white_pillow,
        display_name="Pillow Test",
        thumb="zero_white_pillow",
        group="pillows",
        select_dlg=[
            "Only Test~"
        ]
    )