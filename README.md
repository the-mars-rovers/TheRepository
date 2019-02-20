# Turtlebot: Mars rover

## Links

+ Website: <https://marsrover.space>
+ Github: <https://github.com/the-mars-rovers>
+ Project management: <https://github.com/orgs/the-mars-rovers/projects/1?fullscreen=true>
+ Poster: <https://marsrover.space/poster.pdf>

## Our mission

1. Scan 360° for POIs
2. Drive to selected POI
    + Map environment
3. "Collect" sample
4. Back to 1

## Design

 Perception | Decision     | Actuation
------------|--------------|--------------------------
 3D camera  | Raspberry PI | Control wheels & Gripper

## Timeline

A rough timeline:

```text
Owner   Task                    20/2 27/3  6/3 13/3 20/3 27/3  3/4 *** 24/4  1/5
D       Project Management       ##   --   --   --   --   --   --   --   --   --
        Hardware introduction    ##   ##
C       Motor actuation               ##   ##
R       Acquire image stream          ##   ##
R       Detecting POIs                     ##   ##   ##
J       Terrain mapping                    ##   ##   ##   ##
L       Pathfinding                                  ##   ##   ##   ##
D       Integration                        --   --   --   --   --   --   --   --

***: Easter
```

See project management link for up to date info & progress.
