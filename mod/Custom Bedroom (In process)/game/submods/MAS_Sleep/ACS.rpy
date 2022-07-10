# Special thanks to RaVen for a template
#Atom is not here.

################################################################################
## Objets Selector (ACS)
################################################################################

init -99 python in mas_selspr:

    # acs type data
    PROMPT_MAP["objets"] = {
        "_ev": "objets_acs_test",
        "_min-items": 1,
        "change": "Can you place an object?",
        "wear": "Can I place an object?",
    }

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="objets_acs_test",
            category=["bedroom"],
            prompt=store.mas_selspr.get_prompt("objets", "change"),
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.ENAMORED, None)
        ),
        restartBlacklist=True
    )

label objets_acs_test:
    if mas_current_background == submod_background_bedroom_test:
        pass
    else:
        jump nopeplayer
    python:
        acs_bedroom(test=True)
        use_acs = store.mas_selspr.filter_acs(True, group="objets")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("What would you like to put?")
        sel_map = {}

    m 1eua "Sure [player]!"

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=True)

    if not _return:
        m 1eka "Oh, alright."
    return

################################################################################
## Pillow Selector (ACS)
################################################################################

init -99 python in mas_selspr:

    # acs type data
    PROMPT_MAP["pillows"] = {
        "_ev": "pillows_acs_test",
        "_min-items": 1,
        "change": "Can you change your pillow?",
        "wear": "Can I change your pillow?",
    }

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="pillows_acs_test",
            category=["bedroom"],
            prompt=store.mas_selspr.get_prompt("pillows", "change"),
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.ENAMORED, None)
        ),
        restartBlacklist=True
    )

label pillows_acs_test:
    if mas_current_background == submod_background_bedroom_test:
        pass
    else:
        jump nopeplayer
    python:
        acs_bedroom(test=True)
        mas_selspr.json_sprite_unlock(acs_zero_white_pillow)
        use_acs = store.mas_selspr.filter_acs(True, group="pillows")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Which pillow is calling for your attention [player]?")
        sel_map = {}

    m 1eua "Sure [player]!"

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=False)

    if not _return:
        m 1eka "Oh, alright."
    return

################################################################################
## Blanket Selector (ACS)
################################################################################

init -99 python in mas_selspr:

    # acs type data
    PROMPT_MAP["blankets"] = {
        "_ev": "blankets_acs_test",
        "_min-items": 1,
        "change": "Can you change your blanket?",
        "wear": "Can I change your blanket?",
    }

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="blankets_acs_test",
            category=["bedroom"],
            prompt=store.mas_selspr.get_prompt("blankets", "change"),
            pool=True,
            rules={"no_unlock": None},
            aff_range=(mas_aff.ENAMORED, None)
        ),
        restartBlacklist=True
    )

label blankets_acs_test:
    if mas_current_background == submod_background_bedroom_test:
        pass
    else:
        jump nopeplayer
    python:
        acs_bedroom(test=True)
        mas_selspr.json_sprite_unlock(acs_zero_white_blanket)
        use_acs = store.mas_selspr.filter_acs(True, group="blankets")

        mailbox = store.mas_selspr.MASSelectableSpriteMailbox("Which blanket is calling for your attention [player]?")
        sel_map = {}

    m 1eua "Sure [player]!"

    call mas_selector_sidebar_select_acs(use_acs, mailbox=mailbox, select_map=sel_map, add_remover=False)

    if not _return:
        m 1eka "Oh, alright."
    return

label nopeplayer:
    m 1hua "We're not in the bedroom, [player]."
    jump ch30_loop
    return