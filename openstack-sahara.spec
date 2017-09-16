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
BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr >= 1.6
BuildRequires:    systemd-units
BuildRequires:    python-tooz >= 1.28.0
BuildRequires:    python-glanceclient

# config generator
%if 0%{rhosp} == 0
BuildRequires:    python-zmq
%endif
BuildRequires:    python-redis
BuildRequires:    python-oslo-config >= 2:2.3.0
BuildRequires:    python-castellan >= 0.3.1

# test requirements
BuildRequires:    python-testresources
BuildRequires:    python-oslotest
BuildRequires:    python-hacking
BuildRequires:    python-alembic
BuildRequires:    python-cinderclient >= 1.6.0
BuildRequires:    python-flask >= 0.10
BuildRequires:    python-heatclient >= 1.4.0
BuildRequires:    python-jsonschema >= 2.0.0
BuildRequires:    python-keystoneclient >= 1:2.0.0
BuildRequires:    python-keystonemiddleware >= 2.0.0
BuildRequires:    python-paramiko >= 1.13.0
BuildRequires:    python-manilaclient >= 1.3.0
BuildRequires:    python-neutronclient >= 6.3.0
BuildRequires:    python-novaclient >= 2.28.1
BuildRequires:    python-oslo-concurrency >= 2.3.0
BuildRequires:    python-oslo-db >= 4.1.0
BuildRequires:    python-oslo-i18n >= 2.1.0
BuildRequires:    python-oslo-log >= 1.14.0
BuildRequires:    python-oslo-messaging >= 5.2.0
BuildRequires:    python-oslo-policy >= 1.9.0
BuildRequires:    python-oslo-serialization >= 1.10.0
BuildRequires:    python-swiftclient >= 2.2.0
BuildRequires:    python-oslo-utils >= 3.16.0
BuildRequires:    python-routes
BuildRequires:    /usr/bin/ssh-keygen

Requires:         openstack-sahara-common = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-engine = %{epoch}:%{version}-%{release}
Requires:         openstack-sahara-api = %{epoch}:%{version}-%{release}

%description
%{common_desc}

%files
%{_unitdir}/openstack-sahara-all.service
%{_bindir}/sahara-all
%{_bindir}/sahara-image-pack

%post
%systemd_post openstack-sahara-all.service

%preun
%systemd_preun openstack-sahara-all.service

%postun
%systemd_postun_with_restart openstack-sahara-all.service


%package -n python-sahara
Summary:          Sahara Python libraries

Requires:         python-alembic >= 0.8.7
Requires:         python-babel >= 2.3.4
Requires:         python-castellan >= 0.7.0
Requires:         python-cinderclient >= 3.1.0
Requires:         python-eventlet >= 0.18.2
Requires:         python-flask >= 0.10
Requires:         python-glanceclient >= 1:2.8.0
Requires:         python-heatclient >= 1.6.1
Requires:         python-iso8601 >= 0.1.11
Requires:         python-jinja2 >= 2.7
Requires:         python-jsonschema >= 2.0.0
Requires:         python-keystoneauth1 >= 3.1.0
Requires:         python-keystoneclient >= 1:3.8.0
Requires:         python-keystonemiddleware >= 4.12.0
Requires:         python-manilaclient >= 1.12.0
Requires:         python-neutronclient >= 6.3.0
Requires:         python-novaclient >= 1:9.0.0
Requires:         python-oslo-concurrency >= 3.8.0
Requires:         python-oslo-config >= 2:4.0.0
Requires:         python-oslo-context >= 2.14.0
Requires:         python-oslo-db >= 4.24.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-log >= 3.22.0
Requires:         python-oslo-messaging >= 5.24.2
Requires:         python-oslo-middleware >= 3.27.0
Requires:         python-oslo-policy >= 1.23.0
Requires:         python-oslo-rootwrap >= 5.0.0
Requires:         python-oslo-serialization >= 1.10.0
Requires:         python-oslo-service >= 1.10.0
Requires:         python-oslo-utils >= 3.20.0
Requires:         python-paramiko >= 2.0
Requires:         python-pbr >= 2.0.0
Requires:         python-requests >= 2.10.0
Requires:         python-six >= 1.9.0
Requires:         python-sqlalchemy >= 1.0.10
Requires:         python-stevedore >= 1.20.0
Requires:         python-swiftclient >= 3.2.0
Requires:         python-tooz >= 1.47.0
Requires:         python-webob >= 1.7.1
Requires:         /usr/bin/ssh-keygen

%description -n python-sahara
%{common_desc}

This package contains the Sahara Python library.

%files -n python-sahara
%doc README.rst
%license LICENSE
%{python2_sitelib}/sahara
%{python2_sitelib}/sahara-%{upstream_version}-py?.?.egg-info
%exclude %{python2_sitelib}/%{service}/tests


%package -n python-%{service}-tests
Summary:        Sahara tests
Requires:       openstack-%{service} = %{epoch}:%{version}-%{release}

%description -n python-%{service}-tests
%{common_desc}

This package contains the tests of the Sahara Python library.

This package contains the Sahara test files.

%files -n python-%{service}-tests
%license LICENSE
%{python2_sitelib}/%{service}/tests


%package common
Summary:          Components common to all Sahara services

Requires:         python-sahara = %{epoch}:%{version}-%{release}
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
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/policy.json
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/rootwrap.conf
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/api-paste.ini
%config(noreplace) %{_sysconfdir}/sudoers.d/sahara-rootwrap
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-sahara
%{_sysconfdir}/sahara/rootwrap.d/
%{_bindir}/_sahara-subprocess
%{_bindir}/sahara-db-manage
%{_bindir}/sahara-rootwrap
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
BuildRequires:    python-sphinx >= 1.1.2
BuildRequires:    python-openstackdocstheme
BuildRequires:    python-sphinxcontrib-httpdomain

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

%prep
%autosetup -n sahara-%{upstream_version} -S git

# let RPM handle deps
rm -rf {test-,}requirements.txt

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
%{__python2} setup.py build


%if 0%{?with_doc}
# Note: json warnings likely resolved w/ pygments 1.5 (not yet in Fedora)
%{__python2} setup.py build_sphinx -b html
rm -rf html/.{doctrees,buildinfo}
%{__python2} setup.py build_sphinx -b man
%endif

PYTHONPATH=. oslo-config-generator --config-file=tools/config/config-generator.sahara.conf --output-file=etc/sahara/sahara.conf
sed -i 's#^\#api_paste_config.*#api_paste_config = /etc/sahara/api-paste.ini#' etc/sahara/sahara.conf

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-sahara-all.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-sahara-api.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-sahara-engine.service
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-sahara

HOME=%{_sharedstatedir}/sahara
install -d -m 700 %{buildroot}$HOME

install -p -D -m 640 etc/sahara/sahara.conf %{buildroot}%{_sysconfdir}/sahara/sahara.conf
install -D -m 640 etc/sahara/policy.json %{buildroot}%{_sysconfdir}/sahara/policy.json
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
export DISCOVER_DIRECTORY=sahara/tests/unit
%{__python2} setup.py test

%changelog
