%define _empty_manifest_terminate_build 0
%global optflags %{optflags} -O3 -Wno-error=unused-but-set-variable
%global optflags %{optflags} -Wno-error -Wno-implicit-const-int-float-conversion

Name:		vkquake
Version:	1.31.0
Release:	1
Summary:	Quake 1 port using Vulkan instead of OpenGL for rendering
License:	GPL-2.0-or-later
Group:		Games
URL:		https://github.com/Novum/vkQuake
Source:		https://github.com/Novum/vkQuake/archive/%{version}/vkQuake-%{version}.tar.gz
Source100:	appdata.xml
Source101:	%{name}.desktop
Patch0:		vkquake-compile.patch
BuildRequires:	meson
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(flac)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(libmikmod)
BuildRequires:	pkgconfig(opus)
BuildRequires:	pkgconfig(opusfile)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(libmodplug)
BuildRequires:	glslang
BuildRequires:	spirv-tools

%description
vkQuake is a Quake 1 port using Vulkan instead of OpenGL for rendering. 
It is based on the popular QuakeSpasm port and runs all mods compatible with it like Arcane Dimensions or In The Shadows.
Game data must be placed in ~/.vkquake/id1 .

%prep
%autosetup -p1 -n vkQuake-%{version}

# Drop pre-compiled Windows stuff
rm -rf Windows

%build
%meson \
    -Ddo_userdirs=enabled \
    -Dvorbis_lib=vorbis \
    -Dmp3_lib=mad \
    -Duse_codec_wave=enabled \
    -Duse_codec_mp3=enabled \
    -Duse_codec_flac=enabled \
    -Duse_codec_vorbis=enabled \
    -Duse_codec_opus=enabled

%meson_build

%install
install -Dm755 build/vkquake %{buildroot}%{_gamesbindir}/%{name}
mkdir -p %{buildroot}%{_gamesdatadir}/%{name}

install -D -p -m 644 Misc/vkQuake_512.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -D -p -m 644 %{SOURCE100} %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml
install -D -p -m 644 %{SOURCE101} %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
printf '%s\n' "Please download data from https://www.libsdl.org/projects/quake/data/quakesw-1.0.6.tar.gz extract and place in ~/.vkquake/id1 "

%files
%license LICENSE.txt
%doc readme.md Misc/fitzquake080.txt Misc/fitzquake080sdl.txt Misc/fitzquake085.txt
%dir %{_gamesdatadir}/%{name}/
%{_gamesbindir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
