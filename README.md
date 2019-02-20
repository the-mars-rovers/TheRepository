# Turtlebot: Mars rover

<https://marsrover.space>

## Out mission

1. Scan 360° for POIs
2. Drive to selected POI
    + Map environment
3. "Collect" sample
4. Back to 1

## Design

 Perception | Decision     | Actuation
------------|--------------|-----------------------
 3D camera  | Raspberry PI | Motor: Control wheels
            |              | Gripper

## Timeline

A rough timeline:

```text
                            20/2 27/3  6/3 13/3 20/3 27/3  3/4 Etr 24/4  1/5
    Task Management          ##
    Hardware introduction    ##   ##
C   Motor actuation               ##   ##
R   Acquire image stream          ##   ##
R   Detecting POIs                     ##   ##   ##
J   Terrain mapping                    ##   ##   ##   ##
L   Pathfinding                                  ##   ##   ##
D   Integration                        --   --   --   --   --   --   --   --
```

## Press kit

+ [Our poster](poster.pdf)

