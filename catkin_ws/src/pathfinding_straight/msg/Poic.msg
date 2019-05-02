########################################
# Messages
########################################
uint8 seq_num               # sequence number of the message
int32 distance_to_center    # distance to the center of the screen in pixels
                            # middle of the screen is set to 0
                            # right of the screen is positive
                            # left of the screen is negative
                            # range: -180 to +180
bool ok