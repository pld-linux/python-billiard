#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	billiard
Summary:	Multiprocessing Pool Extensions
Summary(pl.UTF-8):	Rozszerzenia puli procesów
Name:		python-%{module}
Version:	3.6.3.0
Release:	2
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/billiard/
Source0:	https://files.pythonhosted.org/packages/source/b/billiard/%{module}-%{version}.tar.gz
# Source0-md5:	49f47bc7c6868e17591d8018d542b984
URL:		https://github.com/celery/billiard
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.752
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 40.0.0
%if %{with tests}
BuildRequires:	python-case >= 1.3.1
BuildRequires:	python-psutil
BuildRequires:	python-pytest
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools >= 40.0.0
%if %{with tests}
BuildRequires:	python3-case >= 1.3.1
BuildRequires:	python3-psutil
BuildRequires:	python3-pytest
%endif
%endif
Requires:	python-modules >= 1:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
billiard is a fork of the Python 2.7 multiprocessing package. The
multiprocessing package itself is a renamed and updated version of R
Oudkerk's pyprocessing package. This standalone variant draws its
fixes/improvements from python-trunk and provides additional bug fixes
and improvements.

%description -l pl.UTF-8
billiard to odgałęzienie pakietu multiprocessing z Pythona 2.7. Pakiet
multiprocessing to uaktualniona wersja pakietu pyprocessing R Oudkerka
ze zmienioną nazwą. Samodzielny wariant czerpie poprawki i
usprawnienia z najświeższego Pythona, ponadto zawiera dodatkowe
poprawki błędów i ulepszenia.

%package -n python3-%{module}
Summary:	Multiprocessing Pool Extensions
Summary(pl.UTF-8):	Rozszerzenia puli procesów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5
%{?noarchpackage}

%description -n python3-%{module}
billiard is a fork of the Python 2.7 multiprocessing package. The
multiprocessing package itself is a renamed and updated version of R
Oudkerk's pyprocessing package. This standalone variant draws its
fixes/improvements from python-trunk and provides additional bug fixes
and improvements.

%description -n python3-%{module} -l pl.UTF-8
billiard to odgałęzienie pakietu multiprocessing z Pythona 2.7. Pakiet
multiprocessing to uaktualniona wersja pakietu pyprocessing R Oudkerka
ze zmienioną nazwą. Samodzielny wariant czerpie poprawki i
usprawnienia z najświeższego Pythona, ponadto zawiera dodatkowe
poprawki błędów i ulepszenia.

%package apidocs
Summary:	API documentation for billiard module
Summary(pl.UTF-8):	Dokumentacja API modułu billiard
Group:		Documentation
%{?noarchpackage}

%description apidocs
API documentation for billiard module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu billiard.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest t/unit
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest t/unit
%endif
%endif

%if %{with doc}
cd Doc
PYTHONPATH=$(pwd)/../build-3/lib \
sphinx-build -b html -d .build/doctrees . .build/html
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/dummy
%{py_sitedir}/%{module}/dummy/*.py[co]
%attr(755,root,root) %{py_sitedir}/_billiard.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.txt LICENSE.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/.build/html/{_static,library,*.html,*.js}
%endif
