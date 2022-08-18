#!/usr/bin/env python3

from LibrarySystem.__main__ import main

if __name__ == '__main__':

    main(
        Flush = True,                # [Default: True], If flush = True, then the buffering of print statements will be disabled.
        HashedPassword = True,       # [Default: True], If true, the password will be stored in the hashed format, otherwise, the password will be stored in the plain text format
        MaximumBorrowAllowed = 5,    # [Default: 5], A member can only borrow maximum 5 books at a time
        PenaltyLateReturn = 0.5,     # [Default: 0.5], Penalty RM0.50 each day after due date
        PrintASCIIArt = True         # [Default: True], If true, the ASCII art will be printed every time after clear screen, see Constants.py for the art-looking
        )
