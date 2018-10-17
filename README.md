The files in this depot are the tools that were used to help produce the game Scrapyard. Scrapyard's gameplay was a 2D fighting game, rendered with Unreal Engine in 3D, that used per-frame hitbox and attackbox data, paired animation, as well as component based attacks.
These were all made during my senior year of college at the University of Southern California in the Fall of 2012 - Spring 2013.

These tools and scripts focus on creating custom support for any of the features.


## Notable Examples
# //maya/scripts/design/HitBox_AttackBox.py
This is the script that designers used to create a UI, edit boxes in Maya, and export the data to .json format for the game to use. It handles serialisation and de-serialisation to work with existing data. This tool allowed for designers to tune the frames per animation that the character could be hit as well as hit the opponents.
Here is the documentation page for usage of the tool: http://mechbrawler.pbworks.com/w/page/52856792/CollisionBox%20Tool
Here is the youtube tutorial video for the minimum viable product to get into the hands of designers: https://www.youtube.com/watch?v=zLqk627y9DA&feature=youtu.be
Looking back at the script, it would have been a better idea to spread this script out across a couple of files for the classes and UI.
There's also a good number of workflow ideas, but this got the job done for our student project :).

# //emailDecorator/*
This library was made to wrap other python code to give notifications back to the tools/tech art team about when a tool had thrown an unhandled exception.
This currently supports e-mails and text messages. Personal data has been modified to remove other devs and fake mine.

# //stubGenerator/*
Basic PyQT GUI that allowed for making assets in our proper directory structure.
The code is split up properly to allow for both a standalone version as well as a Maya invokeable version with no duplicated code.

# //utils/*
Generic helper scripts used both inside and outside of Maya.
