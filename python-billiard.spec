#
# Conditional build:
%bcond_without	doc	# don't build doc
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	billiard
Summary:	Multiprocessing Pool Extensions
Name:		python-%{module}
Version:	3.3.0.21
Release:	1
License:	BSD
Group:		Libraries/Python
Source0:	https://pypi.python.org/packages/source/b/billiard/%{module}-%{version}.tar.gz
# Source0-md5:	5304a48344d8f7e821d06f57da8af1f4
Patch0:		unittest2.patch
URL:		https://github.com/celery/billiard
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.612
%if %{with python2}
BuildRequires:	python-devel >= 2.7
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

%description apidocs
API documentation for %{module}.

%description apidocs -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build --build-base build-2 %{?with_tests:test}

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
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
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
%dir %{py_sitedir}/%{module}/py2
%{py_sitedir}/%{module}/py2/*.py[co]
%dir %{py_sitedir}/%{module}/tests
%{py_sitedir}/%{module}/tests/*.py[co]
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
