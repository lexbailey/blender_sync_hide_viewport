# Blender add on: Synchronise 'Disable in Viewports' with 'Disable in Renders'

By default, in blender, if you animate the "Disable in Renders" property of an object, so that it sometimes is visible on screen, and sometimes isn't, then you can't easily preview your animation.

These are the buttons I'm talking about:

![visibility control buttons in blender UI](disable_render_buttons.png)

As soon as you have a bunch of different things that are all supposed to appear and disappear at specific times, you just see a mess of objects overlapping in the viewport.

This plugin partially solves this problem (while we wait for blender to implement a better solution)

## What you get

These two buttons are added to the 3D view context menu:

![blender's 3D view context menu, showing two new items at the bottom, as added by this add-on](screenshot.png)

Select some objects, and then right click (or whatever you use to summon the context menu) and choose one of these buttons.

When you copy Disable in Renders to Disable in Viewports, you will see that both f-curves now look the same:

![Comparison of the two synchronised f-curves after using this add-on](f_curve_compare.png)

Choosing "Always show in viewports" simply deletes the f-curve for "Disable in Viewports"

## How to install this

 1. Download `sync_hide_viewport.py`
 2. Open the blender add-on manager window (Edit -> Preferences -> Add-ons)
 3. Click the "Install..." button
 4. Select the downloaded `sync_hide_viewport.py` file and click "Install Add-on"

## How to use

Select some objects in a 3D view, right click anywhere in the 3D view, and use the two new menu options:

 - "Copy Disable-in-Renders to Disable-in-Viewports"
 - "Always show in viewports"