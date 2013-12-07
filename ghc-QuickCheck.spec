Summary:	QuickCheck 2 - library for random testing of program properties
Summary(pl.UTF-8):	QuickCheck 2 - biblioteka do losowego testowania właściwości programu
Name:		ghc-QuickCheck
Version:	2.6
Release:	1
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/QuickCheck
Source0:	http://hackage.haskell.org/package/QuickCheck-%{version}/QuickCheck-%{version}.tar.gz
# Source0-md5:	881d546b39c60789e375b2ab3dbce677
URL:		http://hackage.haskell.org/package/QuickCheck/
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-random-prof
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_releq	ghc
Requires:	ghc-random
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddoc files
%define		_noautocompressdoc	*.haddock

%description
This is QuickCheck 2, a library for random testing of program
properties.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę QuickCheck 2, służącą do losowego
testowania właściwości programu.

%package prof
Summary:	Profiling QuickCheck library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca QuickCheck dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description prof
Profiling QuickCheck library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca QuickCheck dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n QuickCheck-%{version}

# it (ghc?) relies on ld.bfd specific options
mkdir -p ld-dir
if [ -x /usr/bin/ld.bfd ]; then
	ln -sf /usr/bin/ld.bfd ld-dir/ld
fi

%build
PATH=$(pwd)/ld-dir:$PATH
runhaskell Setup.lhs configure -v2 --enable-library-profiling \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
rm -rf %{name}-%{version}-doc
%{__mv} $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/QuickCheck.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE README %{name}-%{version}-doc/html
%{_libdir}/%{ghcdir}/package.conf.d/QuickCheck.conf
%dir %{_libdir}/%{ghcdir}/QuickCheck-%{version}
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/*.o
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/QuickCheck-%{version}/*_p.a
%dir %{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test/*.hi
%dir %{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test/QuickCheck
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test/QuickCheck/*.hi

%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/*_p.a
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test/*.p_hi
%{_libdir}/%{ghcdir}/QuickCheck-%{version}/Test/QuickCheck/*.p_hi
