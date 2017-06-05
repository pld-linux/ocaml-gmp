#
# Conditional build:
%bcond_without	ocaml_opt	# build opt (native code)

%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	GMP binding for OCaml
Summary(pl.UTF-8):	Wiązania GMP dla OCamla
Name:		ocaml-gmp
Version:	20120224
Release:	8
License:	LGPL v2+
Group:		Libraries
Source0:	http://www-verimag.imag.fr/~monniaux/download/mlgmp_%{version}.tar.gz
# Source0-md5:	7001db70f5fed91f230b459425129f96
Patch0:		%{name}-make.patch
Patch1:		inttypes.patch
URL:		http://www-verimag.imag.fr/~monniaux/programmes.html.en
BuildRequires:	gmp-devel >= 5.0.1
BuildRequires:	mpfr-devel >= 3.0.1
BuildRequires:	ocaml >= 1:3.11.2
Requires:	gmp >= 5.0.1
Requires:	mpfr >= 3.0.1
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains files needed to run bytecode executables using
MLGMP library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki MLGMP.

%package devel
Summary:	GMP binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania GMP dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
MLGML library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
biblioteki MLGMP.

%prep
%setup -q -n mlgmp
%patch0 -p1
%patch1 -p1

%build
# clean up precompiled files
%{__make} -j1 1clean

%{__make} -j1 \
	%{?with_ocaml_opt:HAS_OPT=1} \
	CC="%{__cc} %{rpmcflags} -fPIC" \
	CFLAGS_MISC="%{rpmcflags} -fPIC -Wall -Wno-unused -Werror" \
	GMP_INCLUDES=

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	%{?with_ocaml_opt:HAS_OPT=1} \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gmp
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gmp/META <<EOF
requires = ""
version = "%{version}"
directory = "+gmp"
archive(byte) = "gmp.cma"
archive(native) = "gmp.cmxa"
linkopts = ""
EOF

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/gmp/gmp.mli

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog FAQ.txt README
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllgmpstub.so

%files devel
%defattr(644,root,root,755)
%doc *.mli
%dir %{_libdir}/ocaml/gmp
%{_libdir}/ocaml/gmp/gmp.cma
%{_libdir}/ocaml/gmp/gmp.cmi
%if %{with ocaml_opt}
%{_libdir}/ocaml/gmp/gmp.a
%{_libdir}/ocaml/gmp/gmp.cmxa
%endif
%{_libdir}/ocaml/gmp/libgmpstub.a
%{_libdir}/ocaml/site-lib/gmp
