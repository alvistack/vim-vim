%global debug_package %{nil}

Name: vim
Epoch: 100
Version: 8.2.3452
Release: 1%{?dist}
Summary: Vi IMproved
License: MIT
URL: https://github.com/vim/vim/releases
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: fdupes
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: glibc-static
BuildRequires: libXt-devel
BuildRequires: libtool
BuildRequires: ncurses-devel
BuildRequires: pkgconfig

%description
Vim (Vi IMproved) is an almost compatible version of the UNIX editor vi.
Almost every possible command can be performed using only ASCII
characters. Only the 'Q' command is missing (you do not need it). Many
new features have been added: multilevel undo, command line history,
file name completion, block operations, and editing of binary data.

%package -n xxd
Summary: Tool to make (or reverse) a hex dump

%description -n xxd
xxd creates a hex dump of a given file or standard input. It can also
convert a hex dump back to its original binary form.

%package common
Summary: The common files needed by any version of the VIM editor
Requires: xxd = %{epoch}:%{version}-%{release}
Provides: vim-common-devel = %{epoch}:%{version}-%{release}
Provides: vim-data = %{epoch}:%{version}-%{release}
Provides: vim-data-common = %{epoch}:%{version}-%{release}
Provides: vim-filesystem = %{epoch}:%{version}-%{release}
Provides: vim-spell = %{epoch}:%{version}-%{release}
Conflicts: vim-minimal < %{epoch}:%{version}-%{release}

%description common
The vim-common package contains files which every VIM binary will need
in order to run.

%package minimal
Summary: A minimal version of the VIM editor
Requires: vim-common = %{epoch}:%{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
Provides: editor
Provides: vi = %{epoch}:%{version}-%{release}
Provides: vim-small = %{epoch}:%{version}-%{release}
Provides: vim-tiny = %{epoch}:%{version}-%{release}
Provides: %{_bindir}/vi
Conflicts: vim-enhanced < %{epoch}:%{version}-%{release}

%description minimal
The vim-minimal package includes a minimal version of VIM, providing the
commands vi, view, ex, rvi, and rview. NOTE: The online help is only
available when the vim-common package is installed.

%package enhanced
Summary: A version of the VIM editor which includes recent enhancements
Requires: vim-common = %{epoch}:%{version}-%{release}
Requires: vim-minimal = %{epoch}:%{version}-%{release}
Requires(post): %{_sbindir}/update-alternatives
Requires(preun): %{_sbindir}/update-alternatives
Provides: editor
Provides: vim = %{epoch}:%{version}-%{release}
Provides: %{_bindir}/vim

%description enhanced
The vim-enhanced package contains a version of VIM with extra, recently
introduced features like Python and Perl interpreters.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%configure \
    --disable-pythoninterp \
    --disable-perlinterp \
    --disable-python3interp \
    --with-global-runtime=/usr/share/vim/addons,/etc/vim,$$VIM/vimfiles \
    --without-local-dir
%make_build

%install
%make_install
install -Dpm644 -t %{buildroot}%{_datadir}/vim vimrc
mv %{buildroot}%{_bindir}/vim %{buildroot}%{_bindir}/vim.tiny
ln -fs /usr/bin/vim.tiny %{buildroot}%{_bindir}/vim.basic
rm -rf %{buildroot}%{_bindir}/{vi,view,ex,editor}
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/applications/gvim.desktop
rm -rf %{buildroot}%{_datadir}/vim/vim82/doc
rm -rf %{buildroot}%{_datadir}/vim/vim82/lang
rm -rf %{buildroot}%{_datadir}/vim/vim82/tools/vim132
sed -i 's,^#!/usr/bin/python,#!/usr/bin/python3,g' %{buildroot}%{_datadir}/vim/vim82/tools/demoserver.py
sed -i 's,^#!/usr/bin/nawk,#!/usr/bin/awk,g' %{buildroot}%{_datadir}/vim/vim82/tools/mve.awk
sed -i 's,^#!/usr/bin/env perl,#!/usr/bin/perl,g' %{buildroot}%{_datadir}/vim/vim82/tools/pltags.pl
sed -i 's,^#!/usr/bin/env perl,#!/usr/bin/perl,g' %{buildroot}%{_datadir}/vim/vim82/tools/shtags.pl
sed -i 's,^#!/usr/bin/env perl,#!/usr/bin/perl,g' %{buildroot}%{_datadir}/vim/vim82/tools/efm_filter.pl
ln -fs %{_sysconfdir}/alternatives/vi %{buildroot}%{_bindir}/vi
ln -fs %{_sysconfdir}/alternatives/vim %{buildroot}%{_bindir}/vim
ln -fs %{_sysconfdir}/alternatives/view %{buildroot}%{_bindir}/view
ln -fs %{_sysconfdir}/alternatives/ex %{buildroot}%{_bindir}/ex
ln -fs %{_sysconfdir}/alternatives/editor %{buildroot}%{_bindir}/editor
%fdupes -s %{buildroot}%{_prefix}

%post minimal
%{_sbindir}/update-alternatives \
    --install %{_bindir}/vim ex %{_bindir}/vim.tiny 15
%{_sbindir}/update-alternatives \
    --install %{_bindir}/editor ex %{_bindir}/vim.tiny 15
%{_sbindir}/update-alternatives \
    --install %{_bindir}/ex ex %{_bindir}/vim.tiny 15
%{_sbindir}/update-alternatives \
    --install %{_bindir}/vi ex %{_bindir}/vim.tiny 15
%{_sbindir}/update-alternatives \
    --install %{_bindir}/view view %{_bindir}/vim.tiny 15

%preun minimal
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives \
        --remove vim %{_bindir}/vim.tiny
    %{_sbindir}/update-alternatives \
        --remove editor %{_bindir}/vim.tiny
    %{_sbindir}/update-alternatives \
        --remove ex %{_bindir}/vim.tiny
    %{_sbindir}/update-alternatives \
        --remove vi %{_bindir}/vim.tiny
    %{_sbindir}/update-alternatives \
        --remove view %{_bindir}/vim.tiny
fi

%post enhanced
%{_sbindir}/update-alternatives \
    --install %{_bindir}/vim ex %{_bindir}/vim.basic 30
%{_sbindir}/update-alternatives \
    --install %{_bindir}/editor ex %{_bindir}/vim.basic 30
%{_sbindir}/update-alternatives \
    --install %{_bindir}/ex ex %{_bindir}/vim.basic 30
%{_sbindir}/update-alternatives \
    --install %{_bindir}/vi ex %{_bindir}/vim.basic 30
%{_sbindir}/update-alternatives \
    --install %{_bindir}/view view %{_bindir}/vim.basic 30

%preun enhanced
if [ $1 = 0 ]; then
    %{_sbindir}/update-alternatives \
        --remove vim %{_bindir}/vim.basic
    %{_sbindir}/update-alternatives \
        --remove editor %{_bindir}/vim.basic
    %{_sbindir}/update-alternatives \
        --remove ex %{_bindir}/vim.basic
    %{_sbindir}/update-alternatives \
        --remove vi %{_bindir}/vim.basic
    %{_sbindir}/update-alternatives \
        --remove view %{_bindir}/vim.basic
fi

%files -n xxd
%{_bindir}/xxd

%files common
%license LICENSE
%dir %{_datadir}/vim
%dir %{_datadir}/vim/vim82
%{_datadir}/applications/vim.desktop
%{_datadir}/icons/*
%{_datadir}/vim/vim82/*.vim
%{_datadir}/vim/vim82/autoload
%{_datadir}/vim/vim82/colors
%{_datadir}/vim/vim82/compiler
%{_datadir}/vim/vim82/ftplugin
%{_datadir}/vim/vim82/indent
%{_datadir}/vim/vim82/keymap
%{_datadir}/vim/vim82/macros
%{_datadir}/vim/vim82/pack
%{_datadir}/vim/vim82/plugin
%{_datadir}/vim/vim82/print
%{_datadir}/vim/vim82/rgb.txt
%{_datadir}/vim/vim82/spell
%{_datadir}/vim/vim82/syntax
%{_datadir}/vim/vim82/tools
%{_datadir}/vim/vim82/tutor
%{_datadir}/vim/vimrc

%files minimal
%ghost %{_sysconfdir}/alternatives/editor
%ghost %{_sysconfdir}/alternatives/ex
%ghost %{_sysconfdir}/alternatives/vi
%ghost %{_sysconfdir}/alternatives/view
%ghost %{_sysconfdir}/alternatives/vim
%{_bindir}/editor
%{_bindir}/ex
%{_bindir}/rview
%{_bindir}/vi
%{_bindir}/view
%{_bindir}/vim.tiny
%{_datadir}/vim/vim82/defaults.vim

%files enhanced
%{_bindir}/rvim
%{_bindir}/vim
%{_bindir}/vim.basic
%{_bindir}/vimdiff
%{_bindir}/vimtutor

%changelog
