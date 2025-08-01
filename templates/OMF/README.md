# Oh My Font Template
**v2021.10.26**
- A powerful font module template for [Magisk](https://github.com/topjohnwu/Magisk). Powered by [OMF](https://gitlab.com/nongthaihoang/oh_my_font).
- The template includes many useful variables and functions. It is designed intended mostly for font module makers and developers.
- The template alone does nothing. You have to write your own code to make it works.
- Clone/download the repo and edit the `customize.sh`.

## Variables
**ORIGINAL Paths** @ `magisk --path`

| Variable | Value |
| - | - |
| `ORIPRDFONT` | `/product/fonts` |
| `ORIPRDETC` | `/product/etc` |
| `ORIPRDXML` | `/product/etc/fonts_customization.xml` |
| `ORISYSFONT` | `/system/fonts` |
| `ORISYSETC` | `/system/etc` |
| `ORISYSEXTETC` | `/system/system_ext/etc` |
| `ORISYSXML` | `/system/etc/fonts.xml` |

**MODULE Paths** @ `$MODPATH`

| Variable | Value |
| - | - |
| `PRDFONT` | `/system/product/fonts` |
| `PRDETC` | `/system/product/etc` |
| `PRDXML` | `/system/product/etc/fonts_customization.xml` |
| `SYSFONT` | `/system/fonts` |
| `SYSETC` | `/system/etc` |
| `SYSEXTETC` | `/system/system_ext/etc` |
| `SYSXML` | `/system/etc/fonts.xml` |
| `MODPROP` | `/module.prop` |
| `FONTS` | `/fonts` |

**FONTS** @ `fonts.xml`

| Variable | Value |
| - | - |
| `SA` | `sans-serif` |
| `SC` | `sans-serif-condensed` |
| `MO` | `monospace` |
| `SE` | `serif` |
| `SO` | `serif-monospace` |
| `SS` | Sans Serif VF |
| `SSI` | Sans Serif Italic VF |
| `SER` | Serif VF |
| `SERI` | Serif Italic VF |
| `MS` | Monospace VF |
| `MSI` | Monospace Italic VF |
| `SRM` | Serif Monospace VF |
| `SRMI` | Serif Monospace Italic VF |

**Others**

| Variable | Value |
| - | - |
| `OMFDIR` | `/sdcard/OhMyFont ` |

## Functions
**`ver`** (version)
  - Append text to the version string which shows in Magisk app.  
  - Usage: `ver <text>`

**`xml`**
  - Shortcut for the `sed` command to edit fontxml `$XML` (default is `$SYSXML`).  
  - Usage: `xml <sed expresions>`

**`src`** (source)
  - Source (execute) custom scripts (`.sh` files) in  `$OMFDIR`

**`cpf`** (copy font)
  - copy (do not overwrite) fonts from `$FONTS` to `$CPF` (default is `$SYSFONT`).
  - Usage: `cpf [<font_name> ...]`
  - E.g. `cpf font1.ttf font2.ttf font3.otf`

**`fallback`**
  - Make a font family fallback.  
  - Usage: `fallback [font_family]`  
      If no argument is provided, the font family will be `sans-serif` by default.  
  - E.g.  
      `fallback`  
      `fallback serif`  
      It recommends to call the variable `$FB` which is a shortcut for this function. `$FB` will be empty if the fontxml is already patched (i.e. Oxygen 11).

**`prep`** (prepare)
  - Copy the original fontxml `$ORIFONTXML` to module path `$SYSFONTXML` and check if it is patched. This is usually the first function you want to call.  

**`font`**
  - The most powerful function to manipulate `<font>` tag inside a fontxml.  
  - Usage: `font <font_family> <font_name> <font_style> [axis value ...]`
  - `font_family`: `sans-serif`, `serif`, `monospace`, etc  
  - `font_name`: Regular.ttf, Medium.ttf, MyFontName.ttf  
  - `font_style` (from Thin to Black)
    - Uprights: `t`, `el`, `l`, `r`, `m`, `sb`, `b`, `eb`, `bl`  
    - Italics: `ti`, `eli`, `li`, `ri`, `mi`, `sbi`, `bi`, `ebi`, `bli`  
  - `axis`: wdth, wght, slnt, opsz, etc.
  - `value`: value corresponds to each `axis`
  - E.g.  
      `font sans-serif MyFont-Regular.ttf r`  
      `font serif MyFont-Bold.ttf b`  
      `font sans-serif AnyFont-VF.ttf bl wght 900 width 100`  

**`mksty`** (make style)
  - Edit fontxml to add more font styles for a family. Only usefull if your font has more weights than default.  
  - Usage: `mksty [font_family] <max_weight> [min_weight]`  
      without any arguments, `font_family` will be `sans-serif` and `max_weigt` is 9 by default.
  - E.g.  
      `mksty`  
      will make 9 weights for `sans-serif` - both uprights and italics (18 styles). Use this if your font has full weights.  
      `mksty $SC 9`  
      does the same thing but for `sans-serif-condensed` family

**`finish`**
  - Remove all unnecessary files except folder `system` and file `module.prop`, correct permissions. Run it as the last function.  

**`config`**
  - Copy the default config file to `/sdcard/OhMyFont/config.cfg`.

**`valof`** (value of)
  - Read the value of a variable in the config file.  
  - Usage: `valof <variable>`  
  - E.g. `MyVar=$(valof MyVar)`

**`rom`**
  - Try to make the module work system-wide on a ROMs that already uses custom fonts by default. This function is only made for font family `sans-serif`. Do NOT use it if changing any other font families. Call this function before `finish`.  

**`install_font`**
  - You need at least one `Regular.ttf` for static font or one variable font in folder `fonts` `$FONTS` to use this function. It will install font family `sans-serif` and `sans-serif-condensed`. 

**`bold`**
  - A font option for `sans-serif` to replace `Regular` style with `Medium` one. It will read the `BOLD` value in the config file. Run this function after `rom`.  

## How to use
For people who don't know where to start:

### Static fonts
- Put your fonts into `fonts` folder. Rename them as below:  
    - **sans-serif**:
        ```
        BlackItalic.ttf      or bli.ttf
        Black.ttf            or bl.ttf
        ExtraBoldItalic.ttf  or ebi.ttf
        ExtraBold.ttf        or eb.ttf
        BoldItalic.ttf       or bi.ttf
        Bold.ttf             or b.ttf
        SemiBoldItalic.ttf   or sbi.ttf
        SemiBold.ttf         or sb.ttf
        MediumItalic.ttf     or mi.ttf
        Medium.ttf           or m.ttf
        Italic.ttf           or i.ttf
        Regular.ttf          or r.ttf
        LightItalic.ttf      or li.ttf
        Light.ttf            or l.ttf
        ExtraLightItalic.ttf or eli.ttf
        ExtraLight.ttf       or el.ttf
        ThinItalic.ttf       or ti.ttf
        Thin.ttf             or t.ttf
        
        Condensed-BlackItalic.ttf.ttf  or cbli.ttf
        Condensed-Black.ttf            or cbl.ttf
        Condensed-ExtraBoldItalic.ttf  or cebi.ttf
        Condensed-ExtraBold.ttf        or ceb.ttf
        Condensed-BoldItalic.ttf       or cbi.ttf
        Condensed-Bold.ttf             or cb.ttf
        Condensed-SemiBoldItalic.ttf   or csbi.ttf
        Condensed-SemiBold.ttf         or csb.ttf
        Condensed-MediumItalic.ttf     or cmi.ttf
        Condensed-Medium.ttf           or cm.ttf
        Condensed-Italic.ttf           or ci.ttf
        Condensed-Regular.ttf          or cr.ttf
        Condensed-LightItalic.ttf      or cli.ttf
        Condensed-Light.ttf            or cl.ttf
        Condensed-ExtraLightItalic.ttf or celi.ttf
        Condensed-ExtraLight.ttf       or cel.ttf
        Condensed-ThinItalic.ttf       or cti.ttf
        Condensed-Thin.ttf             or ct.ttf
        ```
    - **monospace**: `Mono.ttf` or `mo.ttf`
    - There must be at least one font `Regular.ttf` or `r.ttf`, the rest are optional.  
- Add the following line to the bottom of the `customize.sh` script (or just uncomment them):  
    ```
    prep; $FB; config; install_font; src; rom; bold; finish
    ```

### Variable fonts (VF)
- Usually you'll need two fonts, one for **upright** and the other for **italic**.  
    - Open the config file, at the bottom, set `SS=<upright_font_name>` (e.g. `SS=MyFont-VF.ttf`) and `SSI=<italic_font_name>` (e.g. `SSI=MyFontItalic-VF.ttf`).  
    - If there is only one upright font, just leave the `SSI` empty.
    - Copy your fonts to the folder `fonts`.
- In the config file, set each font style from Thin to Black, from Upright to Condensed with desired axes and values. E.g.
    ```
    ...
    UR  = wght 400
    UBL = wght 900
    ...
    ISB = wght 600 slnt 1
    IL  = wght 300 slnt 1
    ...
    CM  = wght 500 wdth 75
    CT  = wght 100 wdth 75
    ...
    DEB = wght 800 wdth 75 slnt 1
    ...
    ```
    - If you have only upright font, just set upright font styles, leave other font styles (i.e. italics, condensed). They will take the value from upright if needed.
    - Only set font styles that your fonts actually support and do not set the same value for different font styles (e.g.  `UT = wght 400` `UR = wgth 400`).
- The final step is the same as for static fonts.

## Support
- [XDA](https://forum.xda-developers.com/t/module-oh-my-font-improve-android-typography.4215515)
