%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2426b928085a020d8a90d0d879ab7008d0896c8a
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
Source2:       openstack-sahara-api.service
Source3:       openstack-sahara-engine.service
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:     noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr >= 3.1.1
BuildRequires:    systemd
BuildRequires:    python3-tooz >= 1.58.0
BuildRequires:    openstack-macros
BuildRequires:    python3-glanceclient

# config generator
BuildRequires:    python3-oslo-config >= 2:6.8.0
BuildRequires:    python3-castellan >= 0.16.0

# test requirements
# python2-testresources still required by oslo.db tests
BuildRequires:    python3-testresources
BuildRequires:    python3-stestr >= 1.0.0
BuildRequires:    python3-testscenarios
BuildRequires:    python3-oslotest
BuildRequires:    python3-hacking
BuildRequires:    python3-alembic
BuildRequires:    python3-botocore >= 1.5.1
BuildRequires:    python3-cinderclient >= 3.3.0
BuildRequires:    python3-heatclient >= 1.10.0
BuildRequires:    python3-jsonschema >= 2.6.0
BuildRequires:    python3-keystoneclient >= 1:3.8.0
BuildRequires:    python3-keystonemiddleware >= 4.17.0
BuildRequires:    python3-paramiko >= 2.0.0
BuildRequires:    python3-manilaclient >= 1.16.0
BuildRequires:    python3-microversion-parse >= 0.2.1
BuildRequires:    python3-neutronclient >= 6.7.0
BuildRequires:    python3-novaclient >= 9.1.0
BuildRequires:    python3-oslo-concurrency >= 3.26.0
BuildRequires:    python3-oslo-db >= 4.27.0
BuildRequires:    python3-oslo-i18n >= 3.20.0
BuildRequires:    python3-oslo-log >= 5.0.0
BuildRequires:    python3-oslo-messaging >= 5.29.0
BuildRequires:    python3-oslo-policy >= 1.30.0
BuildRequires:    python3-oslo-serialization >= 2.25.0
BuildRequires:    python3-oslo-upgradecheck >= 0.1.0
BuildRequires:    python3-swiftclient >= 3.2.0
BuildRequires:    python3-oslo-utils >= 3.33.0
BuildRequires:    python3-routes
BuildRequires:    /usr/bin/ssh-keygen
BuildRequires:    /usr/bin/pathfix.py
%if 0%{rhosp} == 0
BuildRequires:    python3-zmq
%endif
BuildRequires:    python3-redis
BuildRequires:    python3-flask >= 2.1.2

Requires:         openstack-sahara-common = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-engine = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-api = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-image-pack = %{epoch}:%{version}-%{release}

%description
%{common_desc}

%files
%doc README.rst
%license LICENSE


%package -n python3-sahara
Summary:          Sahara Python libraries
%{?python_provide:%python_provide python3-sahara}

Requires:         python3-alembic >= 0.9.6
Requires:         python3-botocore >= 1.5.1
Requires:         python3-castellan >= 0.16.0
Requires:         python3-cinderclient >= 3.3.0
Requires:         python3-eventlet >= 0.26.0
Requires:         python3-glanceclient >= 2.8.0
Requires:         python3-heatclient >= 1.10.0
Requires:         python3-iso8601 >= 0.1.11
Requires:         python3-jinja2 >= 2.10
Requires:         python3-jsonschema >= 3.2.0
Requires:         python3-keystoneauth1 >= 3.4.0
Requires:         python3-keystoneclient >= 1:3.8.0
Requires:         python3-keystonemiddleware >= 4.17.0
Requires:         python3-manilaclient >= 1.16.0
Requires:         python3-microversion-parse >= 0.2.1
Requires:         python3-neutronclient >= 6.7.0
Requires:         python3-novaclient >= 9.1.0
Requires:         python3-oslo-concurrency >= 3.26.0
Requires:         python3-oslo-config >= 2:6.8.0
Requires:         python3-oslo-context >= 2.22.0
Requires:         python3-oslo-db >= 6.0.0
Requires:         python3-oslo-i18n >= 3.20.0
Requires:         python3-oslo-log >= 5.0.0
Requires:         python3-oslo-messaging >= 10.2.0
Requires:         python3-oslo-middleware >= 3.31.0
Requires:         python3-oslo-policy >= 3.6.0
Requires:         python3-oslo-rootwrap >= 5.8.0
Requires:         python3-oslo-serialization >= 2.25.0
Requires:         python3-oslo-service >= 1.31.0
Requires:         python3-oslo-upgradecheck >= 1.3.0
Requires:         python3-oslo-utils >= 4.5.0
Requires:         python3-paramiko >= 2.7.1
Requires:         python3-pbr >= 3.1.1
Requires:         python3-requests >= 2.23.0
Requires:         python3-sqlalchemy >= 1.0.10
Requires:         python3-stevedore >= 1.20.0
Requires:         python3-swiftclient >= 3.2.0
Requires:         python3-tooz >= 1.58.0
Requires:         python3-webob >= 1.7.1
Requires:         /usr/bin/ssh-keygen
Requires:         python3-flask >= 2.0.1
Requires:         python3-libguestfs

%description -n python3-sahara
%{common_desc}

This package contains the Sahara Python library.

%files -n python3-sahara
%doc README.rst
%license LICENSE
%{python3_sitelib}/sahara
%{python3_sitelib}/sahara-%{upstream_version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/%{service}/tests


%package -n python3-%{service}-tests
Summary:        Sahara tests
%{?python_provide:%python_provide python3-%{service}-tests}
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python3-%{service}-tests
%{common_desc}

This package contains the Sahara test files.

%files -n python3-%{service}-tests
%license LICENSE
%{python3_sitelib}/%{service}/tests


%package common
Summary:          Components common to all Sahara services

Requires:         python3-sahara = %{epoch}:%{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif
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
BuildRequires:    python3-sphinx >= 1.6.2
BuildRequires:    python3-openstackdocstheme >= 1.18.1
BuildRequires:    python3-sphinxcontrib-httpdomain


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

Requires:         python3-sahara = %{epoch}:%{version}-%{release}
Requires:         python3-libguestfs

%description image-pack
%{common_desc}

This package contains the sahara-image-pack program.

%files image-pack
%{_bindir}/sahara-image-pack


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
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

%build
%{py3_build}


%if 0%{?with_doc}
export PYTHONPATH=.
# Note: json warnings likely resolved w/ pygments 1.5 (not yet in Fedora)
sphinx-build -W -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build -W -b man doc/source doc/build/man
%endif

PYTHONPATH=. oslo-config-generator --config-file=tools/config/config-generator.sahara.conf --output-file=etc/sahara/sahara.conf
sed -i 's#^\#api_paste_config.*#api_paste_config = /etc/sahara/api-paste.ini#' etc/sahara/sahara.conf

%install
%{py3_install}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-sahara-api.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-sahara-engine.service
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-sahara

HOME=%{_sharedstatedir}/sahara
install -d -m 700 %{buildroot}$HOME

install -p -D -m 640 etc/sahara/sahara.conf %{buildroot}%{_sysconfdir}/sahara/sahara.conf
install -p -D -m 640 etc/sahara/rootwrap.conf %{buildroot}%{_sysconfdir}/sahara/rootwrap.conf
install -p -D -m 640 etc/sahara/api-paste.ini %{buildroot}%{_sysconfdir}/sahara/api-paste.ini
install -p -D -m 440 etc/sudoers.d/sahara-rootwrap %{buildroot}%{_sysconfdir}/sudoers.d/sahara-rootwrap

# sahara-all is deprecated upstream, probably broken and
# thus not packaged anymore
rm -f %{buildroot}%{_prefix}/bin/sahara-all

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

# Fix ambiguous shebangs
# NOTE(jpena): once the sahara plugins are removed, this will need to be removed too
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}%{python3_sitelib}/sahara/plugins/

%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 doc/build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

%check
# Remove hacking tests, we don't need them
rm sahara/tests/unit/utils/test_hacking.py
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD
export PYTHON=%{__python3}
stestr run

%changelog
