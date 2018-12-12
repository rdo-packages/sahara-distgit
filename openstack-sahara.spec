# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
# Globals Declaration

%global service sahara
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sahara_user sahara
%global sahara_group %{sahara_user}
%global with_doc 1
# guard for packages OSP does not ship
%global rhosp 0

%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}}
%endif

%global common_desc \
Sahara provides the ability to elastically manage Apache Hadoop clusters on \
OpenStack.

Name:          openstack-sahara
# Liberty semver reset
# https://review.openstack.org/#/q/I6a35fa0dda798fad93b804d00a46af80f08d475c,n,z
Epoch:         1
Version:       XXX
Release:       XXX
Provides:      openstack-savanna
Summary:       Apache Hadoop cluster management on OpenStack
License:       ASL 2.0
URL:           https://launchpad.net/sahara
Source0:       https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
Source1:       sahara.logrotate
Source2:       openstack-sahara-all.service
Source3:       openstack-sahara-api.service
Source4:       openstack-sahara-engine.service
BuildArch:     noarch

BuildRequires:    git
BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-setuptools
BuildRequires:    python%{pyver}-pbr >= 2.0.0
BuildRequires:    systemd
BuildRequires:    python%{pyver}-tooz >= 1.58.0
BuildRequires:    openstack-macros
BuildRequires:    python%{pyver}-glanceclient

# config generator
BuildRequires:    python%{pyver}-oslo-config >= 2:5.2.0
BuildRequires:    python%{pyver}-castellan >= 0.16.0

# test requirements
# python2-testresources still required by oslo.db tests
BuildRequires:    python%{pyver}-testresources
BuildRequires:    python%{pyver}-stestr >= 1.0.0
BuildRequires:    python%{pyver}-testscenarios
BuildRequires:    python%{pyver}-oslotest
BuildRequires:    python%{pyver}-hacking
BuildRequires:    python%{pyver}-alembic
BuildRequires:    python%{pyver}-botocore >= 1.5.1
BuildRequires:    python%{pyver}-cinderclient >= 3.3.0
BuildRequires:    python%{pyver}-heatclient >= 1.10.0
BuildRequires:    python%{pyver}-jsonschema >= 2.6.0
BuildRequires:    python%{pyver}-keystoneclient >= 1:3.8.0
BuildRequires:    python%{pyver}-keystonemiddleware >= 4.17.0
BuildRequires:    python%{pyver}-paramiko >= 2.0.0
BuildRequires:    python%{pyver}-manilaclient >= 1.16.0
BuildRequires:    python%{pyver}-neutronclient >= 6.7.0
BuildRequires:    python%{pyver}-novaclient >= 9.1.0
BuildRequires:    python%{pyver}-oslo-concurrency >= 3.26.0
BuildRequires:    python%{pyver}-oslo-db >= 4.27.0
BuildRequires:    python%{pyver}-oslo-i18n >= 3.15.3
BuildRequires:    python%{pyver}-oslo-log >= 3.36.0
BuildRequires:    python%{pyver}-oslo-messaging >= 5.29.0
BuildRequires:    python%{pyver}-oslo-policy >= 1.30.0
BuildRequires:    python%{pyver}-oslo-serialization >= 2.18.0
BuildRequires:    python%{pyver}-oslo-upgradecheck >= 0.1.0
BuildRequires:    python%{pyver}-swiftclient >= 3.2.0
BuildRequires:    python%{pyver}-oslo-utils >= 3.33.0
BuildRequires:    python%{pyver}-routes
BuildRequires:    /usr/bin/ssh-keygen

# Handle python2 exception
%if %{pyver} == 2
%if 0%{rhosp} == 0
BuildRequires:    python-zmq
%endif
BuildRequires:    python-redis
BuildRequires:    python-flask >= 1:1.0.2
BuildRequires:    python-sphinxcontrib-httpdomain
%else
%if 0%{rhosp} == 0
BuildRequires:    python%{pyver}-zmq
%endif
BuildRequires:    python%{pyver}-redis
BuildRequires:    python%{pyver}-flask >= 1:1.0.2
BuildRequires:    python%{pyver}-sphinxcontrib-httpdomain
%endif

Requires:         openstack-sahara-common = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-engine = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-api = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-image-pack = %{epoch}:%{version}-%{release}

%description
%{common_desc}

%files
%{_unitdir}/openstack-sahara-all.service
%{_bindir}/sahara-all

%post
%systemd_post openstack-sahara-all.service

%preun
%systemd_preun openstack-sahara-all.service

%postun
%systemd_postun_with_restart openstack-sahara-all.service


%package -n python%{pyver}-sahara
Summary:          Sahara Python libraries
%{?python_provide:%python_provide python%{pyver}-sahara}

Requires:         python%{pyver}-alembic >= 0.8.10
Requires:         python%{pyver}-babel >= 2.3.4
Requires:         python%{pyver}-botocore >= 1.5.1
Requires:         python%{pyver}-castellan >= 0.16.0
Requires:         python%{pyver}-cinderclient >= 3.3.0
Requires:         python%{pyver}-eventlet >= 0.18.2
Requires:         python%{pyver}-glanceclient >= 2.8.0
Requires:         python%{pyver}-heatclient >= 1.10.0
Requires:         python%{pyver}-iso8601 >= 0.1.11
Requires:         python%{pyver}-jinja2 >= 2.10
Requires:         python%{pyver}-jsonschema >= 2.6.0
Requires:         python%{pyver}-keystoneauth1 >= 3.4.0
Requires:         python%{pyver}-keystoneclient >= 1:3.8.0
Requires:         python%{pyver}-keystonemiddleware >= 4.17.0
Requires:         python%{pyver}-manilaclient >= 1.16.0
Requires:         python%{pyver}-neutronclient >= 6.7.0
Requires:         python%{pyver}-novaclient >= 9.1.0
Requires:         python%{pyver}-oslo-concurrency >= 3.26.0
Requires:         python%{pyver}-oslo-config >= 2:5.2.0
Requires:         python%{pyver}-oslo-context >= 2.19.2
Requires:         python%{pyver}-oslo-db >= 4.27.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-log >= 3.36.0
Requires:         python%{pyver}-oslo-messaging >= 5.29.0
Requires:         python%{pyver}-oslo-middleware >= 3.31.0
Requires:         python%{pyver}-oslo-policy >= 1.30.0
Requires:         python%{pyver}-oslo-rootwrap >= 5.8.0
Requires:         python%{pyver}-oslo-serialization >= 2.18.0
Requires:         python%{pyver}-oslo-service >= 1.24.0
Requires:         python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-paramiko >= 2.0.0
Requires:         python%{pyver}-pbr >= 2.0.0
Requires:         python%{pyver}-requests >= 2.14.2
Requires:         python%{pyver}-six >= 1.10.0
Requires:         python%{pyver}-sqlalchemy >= 1.0.10
Requires:         python%{pyver}-stevedore >= 1.20.0
Requires:         python%{pyver}-swiftclient >= 3.2.0
Requires:         python%{pyver}-tooz >= 1.58.0
Requires:         python%{pyver}-webob >= 1.7.1
Requires:         /usr/bin/ssh-keygen

# Handle python2 exception
%if %{pyver} == 2
Requires:         python-flask >= 1:1.0.2
Requires:         python-libguestfs
%else
Requires:         python%{pyver}-flask >= 1:1.0.2
Requires:         python%{pyver}-libguestfs
%endif

%description -n python%{pyver}-sahara
%{common_desc}

This package contains the Sahara Python library.

%files -n python%{pyver}-sahara
%doc README.rst
%license LICENSE
%{pyver_sitelib}/sahara
%{pyver_sitelib}/sahara-%{upstream_version}-py?.?.egg-info
%exclude %{pyver_sitelib}/%{service}/tests


%package -n python%{pyver}-%{service}-tests
Summary:        Sahara tests
%{?python_provide:%python_provide python%{pyver}-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python%{pyver}-%{service}-tests
%{common_desc}

This package contains the Sahara test files.

%files -n python%{pyver}-%{service}-tests
%license LICENSE
%{pyver_sitelib}/%{service}/tests


%package common
Summary:          Components common to all Sahara services

Requires:         python%{pyver}-sahara = %{epoch}:%{version}-%{release}
%{?systemd_requires}
Requires(pre):    shadow-utils

%description common
%{common_desc}

These components are common to all Sahara services.

%pre common
# Origin: http://fedoraproject.org/wiki/Packaging:UsersAndGroups#Dynamic_allocation
USERNAME=%{sahara_user}
GROUPNAME=%{sahara_group}
HOMEDIR=%{_sharedstatedir}/sahara
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
  -c "Sahara Daemons" $USERNAME
exit 0

%files common
%doc README.rst
%license LICENSE
%dir %{_sysconfdir}/sahara
# Note: this file is not readable because it holds auth credentials
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/sahara.conf
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/rootwrap.conf
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/api-paste.ini
%config(noreplace) %{_sysconfdir}/sudoers.d/sahara-rootwrap
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-sahara
%{_sysconfdir}/sahara/rootwrap.d/
%{_bindir}/_sahara-subprocess
%{_bindir}/sahara-db-manage
%{_bindir}/sahara-rootwrap
%{_bindir}/sahara-status
%{_bindir}/sahara-templates
%{_bindir}/sahara-wsgi-api
%dir %attr(-, %{sahara_user}, %{sahara_group}) %{_sharedstatedir}/sahara
%dir %attr(0750, %{sahara_user}, %{sahara_group}) %{_localstatedir}/log/sahara
%{_datarootdir}/sahara/
# Note: permissions on sahara's home are intentionally 0700

%if 0%{?with_doc}


%package doc
Group:         Documentation
Summary:       Usage documentation for the Sahara cluster management API
Requires:      openstack-sahara-common = %{epoch}:%{version}-%{release}
BuildRequires:    python%{pyver}-sphinx >= 1.6.2
BuildRequires:    python%{pyver}-openstackdocstheme >= 1.18.1

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:    python-sphinxcontrib-httpdomain
%else
BuildRequires:    python%{pyver}-sphinxcontrib-httpdomain
%endif


%description doc
%{common_desc}

This documentation provides instructions and examples on how to
install, use, and manage the Sahara infrastructure.

%files doc
%license LICENSE
%doc doc/build/html
%{_mandir}/man1/sahara*.1.gz

%endif


%package engine
Summary:          The Sahara cluster management engine

Requires:         openstack-sahara-common = %{epoch}:%{version}-%{release}

%description engine
%{common_desc}

This package contains the Sahara Engine service.

%files engine
%{_unitdir}/openstack-sahara-engine.service
%{_bindir}/sahara-engine

%post engine
%systemd_post openstack-sahara-engine.service

%preun engine
%systemd_preun openstack-sahara-engine.service

%postun engine
%systemd_postun_with_restart openstack-sahara-engine.service


%package api
Summary:          The Sahara cluster management API

Requires:         openstack-sahara-common = %{epoch}:%{version}-%{release}

%description api
%{common_desc}

This package contains the Sahara API service.

%files api
%{_unitdir}/openstack-sahara-api.service
%{_bindir}/sahara-api

%post api
%systemd_post openstack-sahara-api.service

%preun api
%systemd_preun openstack-sahara-api.service

%postun api
%systemd_postun_with_restart openstack-sahara-api.service


%package image-pack
Summary:          Sahara Image Pack

Requires:         python%{pyver}-sahara = %{epoch}:%{version}-%{release}
# Handle python2 exception
%if %{pyver} == 2
Requires:         python-libguestfs
%else
Requires:         python%{pyver}-libguestfs
%endif

%description image-pack
%{common_desc}

This package contains the sahara-image-pack program.

%files image-pack
%{_bindir}/sahara-image-pack


%prep
%autosetup -n sahara-%{upstream_version} -S git

# let RPM handle deps
%py_req_cleanup

# remove the shbang from these files to suppress rpmlint warnings, these are
# python based scripts that get processed to form the installed shell scripts.
for file in sahara/cli/*.py; do
    sed 1,2d $file > $file.new &&
    touch -r $file $file.new &&
    mv $file.new $file
done
# set executable on these files to suppress rpmlint warnings, they are used as
# templates to create shell scripts.
chmod a+x sahara/plugins/vanilla/hadoop2/resources/post_conf.template
chmod a+x sahara/plugins/spark/resources/spark-env.sh.template
# also set executable on this topology script, should have been set upstream
chmod a+x sahara/plugins/spark/resources/topology.sh

%build
%{pyver_build}


%if 0%{?with_doc}
export PYTHONPATH=.
# Note: json warnings likely resolved w/ pygments 1.5 (not yet in Fedora)
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build-%{pyver} -W -b man doc/source doc/build/man
%endif

PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=tools/config/config-generator.sahara.conf --output-file=etc/sahara/sahara.conf
sed -i 's#^\#api_paste_config.*#api_paste_config = /etc/sahara/api-paste.ini#' etc/sahara/sahara.conf

%install
%{pyver_install}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-sahara-all.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-sahara-api.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-sahara-engine.service
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-sahara

HOME=%{_sharedstatedir}/sahara
install -d -m 700 %{buildroot}$HOME

install -p -D -m 640 etc/sahara/sahara.conf %{buildroot}%{_sysconfdir}/sahara/sahara.conf
install -p -D -m 640 etc/sahara/rootwrap.conf %{buildroot}%{_sysconfdir}/sahara/rootwrap.conf
install -p -D -m 640 etc/sahara/api-paste.ini %{buildroot}%{_sysconfdir}/sahara/api-paste.ini
install -p -D -m 440 etc/sudoers.d/sahara-rootwrap %{buildroot}%{_sysconfdir}/sudoers.d/sahara-rootwrap

# Remove duplicate installations of config files
rm -rf %{buildroot}%{_prefix}/etc

# Install rootwrap files in /usr/share/sahara/rootwrap
mkdir -p %{buildroot}%{_datarootdir}/sahara/rootwrap/
install -p -D -m 644 etc/sahara/rootwrap.d/* %{buildroot}%{_datarootdir}/sahara/rootwrap/
# And add symlink under /etc/sahara/rootwrap.d, because the default config file needs that
mkdir -p %{buildroot}%{_sysconfdir}/sahara/rootwrap.d
for filter in %{buildroot}%{_datarootdir}/sahara/rootwrap/*.filters; do
ln -s %{_datarootdir}/sahara/rootwrap/$(basename $filter) %{buildroot}%{_sysconfdir}/sahara/rootwrap.d/
done

mkdir -p -m0755 %{buildroot}/%{_localstatedir}/log/sahara

%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

%check
# Remove hacking tests, we don't need them
rm sahara/tests/unit/utils/test_hacking.py
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
stestr-%{pyver} run

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/sahara/commit/?id=0b8ab036e7a4b1beedbc8bcd2d33736a9e296536
