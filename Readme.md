```
       .O
      o .
    aaaaaaa
    "8.o 8"
     8. O8
     8 o.8     ooooooooo      ooo ooo                  oooo             .o8
  ,adPO .Yba,  `88'   `8      `88 `88                  `88'            "888
 dP". O  o "Yb  88     .oooo.  88  88  .oooo.  .oooo.o  88      .ooo.  888ooo.
dP' O . o .O`Yb 88oo8 d88'`88b 88  88 d88'`88b d8(  "8  88     `P  )8b d88'`88b
8^^^^^^^^^^^^^8 88  " 888oo888 88  88 888oo888` "Y8b.   88      .oP"88 888  888
Yb,         ,dP 88    888   .o 88  88 888   .oo.  )88b  88    od8(  88 888  888
 "Ya,_____,aP" o88o   `Y8bd8P'o88oo88o`Y8bd8P'8""888P' o88oood8`Y88""8o`Y8od8P'
   `"""""""'


      Python framework for sensor connections and GUI for the "Felles Lab".


                             Sigve Karolius

                   Department of Chemical Engineering
             Norwegian University of Science and Technology

                                .            .
                               / \          / \
                              /   \   /\   /   \
                              |   |  /  \  |   |
                       .______|   |_/    \_|   |______.
                     _/                                \_
          /\        |                                    |        /\
    _____/  \  _____|                                    |_____  /  \_____
             \/                                                \/
```

# Install

## Dependencies

### Ubuntu (Linux)

```
sudo apt install python-serial python-pip qt4-designer qt4-dev-tools pyqt4-dev-tools
sudo pip install minimalmodbus
```

### Mac OSx (FreeBSD)

#### Mac Ports

```
sudo port install qt4-mac qt4-creator-mac py27-pyqt4 py27-pip py27-serial
sudo pip install minimalmodbus
```

### Homebrew

... not tested


## Install Procedure

```
python setup.py build
python setup.py install --prefix="${HOME}"
```


#### Serial to USB Communication ##

[Website]


[website]: https://pbxbook.com/other/mac-tty.html

Most serial-to-USB adapters  require a driver to be installed before working on OS X.

Recommended to try [Prolific PL2303](http://www.prolific.com.tw/US/ShowProduct.aspx?p_id=229&pcid=41) 
driver  first and if that does not work try [Silicon Labs](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers).

