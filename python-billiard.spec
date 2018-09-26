#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_with	tests	# do perform "make test" (downloads external code)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	billiard
Summary:	Multiprocessing Pool Extensions
Name:		python-%{module}
Version:	3.5.0.4
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/b/billiard/%{module}-%{version}.tar.gz
# Source0-md5:	e9558e6969b6e3f48891c2122f365c60
URL:		https://github.com/celery/billiard
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-mock
BuildRequires:	python-nose
%endif
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-nose
%endif
%endif
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
billiard is a fork of the Python 2.7 multiprocessing package. The
multiprocessing package itself is a renamed and updated version of R
Oudkerk's pyprocessing package. This standalone variant is intended to
be compatible with Python 2.4 and 2.5, and will draw its
fixes/improvements from python-trunk.

%package -n python3-%{module}
Summary:	Multiprocessing Pool Extensions
Group:		Libraries/Python
Requires:	python3-modules
BuildArch:	noarch

%description -n python3-%{module}
billiard is a fork of the Python 2.7 multiprocessing package. The
multiprocessing package itself is a renamed and updated version of R
Oudkerk's pyprocessing package. This standalone variant is intended to
be compatible with Python 2.4 and 2.5, and will draw its
fixes/improvements from python-trunk.

%package apidocs
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py_build %{?with_tests:test}

%if %{with doc}
cd Doc
PYTHONPATH=../build-2/lib sphinx-build -b html -d .build/doctrees . .build/html
rm -rf .build/html/_sources
cd ..
%endif
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%py3_build %{?with_tests:test}
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
%doc *.txt README.rst
%dir %{py_sitedir}/%{module}
%{py_sitedir}/%{module}/*.py[co]
%dir %{py_sitedir}/%{module}/dummy
%{py_sitedir}/%{module}/dummy/*.py[co]
%{py_sitedir}/_%{module}.so
%{py_sitedir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc *.txt README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc Doc/.build/html/*
%endif
