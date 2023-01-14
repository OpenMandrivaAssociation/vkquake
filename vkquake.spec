%define _empty_manifest_terminate_build 0

Name:           vkquake
Version:        1.22.3
Release:        1
Summary:        Quake 1 port using Vulkan instead of OpenGL for rendering
License:        GPL-2.0-or-later
Group:          Games
URL:            https://github.com/Novum/vkQuake
Source:         https://github.com/Novum/vkQuake/archive/%{version}/vkQuake-%{version}.tar.gz
Source100:      appdata.xml
Source101:      %{name}.desktop
Patch0:		vkquake-compile.patch

BuildRequires:  vulkan-devel
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(mad)
BuildRequires:  pkgconfig(libmikmod)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(opusfile)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:  cmake(zopfli)
BuildRequires:  zopfli

%description
vkQuake is a Quake 1 port using Vulkan instead of OpenGL for rendering. 
It is based on the popular QuakeSpasm port and runs all mods compatible with it like Arcane Dimensions or In The Shadows.
Game data must be placed in ~/.vkquake/id1 .

%prep
%autosetup -p1 -n vkQuake-%{version}

# Drop pre-compiled Windows stuff
rm -rf Windows

%build
%set_build_flags
# quake
%make_build -C Quake \
    STRIP=": do not strip:" \
    DO_USERDIRS=1 \
    CC=%{__cc} \
    USE_SDL2=1 \
    USE_CODEC_FLAC=1 \
    USE_CODEC_OPUS=1 \
    USE_CODEC_MIKMOD=1 \
    USE_CODEC_UMX=1 \
    USE_CODEC_MP3=0
strip Quake/vkquake
# stuff
%make_build -C Misc/vq_pak

%install
install -Dm755 Quake/vkquake %{buildroot}%{_bindir}/%{name}
install -Dm644 Misc/vq_pak/vkquake.pak %{buildroot}%{_datadir}/games/%{name}/%{name}.pak
install -D -p -m 644 Misc/vkQuake_512.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
install -D -p -m 644 %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%license LICENSE.txt
%doc readme.md Misc/fitzquake080.txt Misc/fitzquake080sdl.txt Misc/fitzquake085.txt
%dir %{_datadir}/games/%{name}/
%{_bindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/games/%{name}/%{name}.pak
%{_datadir}/pixmaps/%{name}.png
