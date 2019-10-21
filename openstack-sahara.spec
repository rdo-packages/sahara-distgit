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
Version:       8.0.2
Release:       1%{?dist}
Provides:      openstack-savanna
Summary:       Apache Hadoop cluster management on OpenStack
License:       ASL 2.0
URL:           https://launchpad.net/sahara
Source0:       https://tarballs.openstack.org/%{service}/%{service}-%{upstream_version}.tar.gz
#

Source1:       sahara.logrotate
Source2:       openstack-sahara-all.service
Source3:       openstack-sahara-api.service
Source4:       openstack-sahara-engine.service
BuildArch:     noarch

BuildRequires:    git
BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pbr >= 1.6
BuildRequires:    systemd
BuildRequires:    python2-tooz >= 1.58.0
BuildRequires:    openstack-macros
BuildRequires:    python2-glanceclient

# config generator
%if 0%{rhosp} == 0
BuildRequires:    python-zmq
%endif
BuildRequires:    python-redis
BuildRequires:    python2-oslo-config >= 2:5.1.0
BuildRequires:    python2-castellan >= 0.16.0

# test requirements
BuildRequires:    python2-testresources
BuildRequires:    python2-testscenarios
BuildRequires:    python2-oslotest
BuildRequires:    python2-hacking
BuildRequires:    python2-alembic
BuildRequires:    python2-botocore >= 1.5.1
BuildRequires:    python2-cinderclient >= 3.3.0
BuildRequires:    python-flask >= 0.10
BuildRequires:    python2-heatclient >= 1.10.0
BuildRequires:    python2-jsonschema >= 2.6.0
BuildRequires:    python2-keystoneclient >= 1:2.0.0
BuildRequires:    python2-keystonemiddleware >= 4.17.0
BuildRequires:    python2-paramiko >= 1.13.0
BuildRequires:    python2-manilaclient >= 1.16.0
BuildRequires:    python2-neutronclient >= 6.3.0
BuildRequires:    python2-novaclient >= 9.1.0
BuildRequires:    python2-oslo-concurrency >= 3.25.0
BuildRequires:    python2-oslo-db >= 4.27.0
BuildRequires:    python2-oslo-i18n >= 3.15.3
BuildRequires:    python2-oslo-log >= 3.36.0
BuildRequires:    python2-oslo-messaging >= 5.29.0
BuildRequires:    python2-oslo-policy >= 1.30.0
BuildRequires:    python2-oslo-serialization >= 2.18.0
BuildRequires:    python2-swiftclient >= 2.2.0
BuildRequires:    python2-oslo-utils >= 3.33.0
BuildRequires:    python2-routes
BuildRequires:    /usr/bin/ssh-keygen

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


%package -n python-sahara
Summary:          Sahara Python libraries

Requires:         python2-alembic >= 0.8.10
Requires:         python2-babel >= 2.3.4
Requires:         python2-botocore >= 1.5.1
Requires:         python2-castellan >= 0.16.0
Requires:         python2-cinderclient >= 3.3.0
Requires:         python2-eventlet >= 0.18.2
Requires:         python-flask >= 0.10
Requires:         python2-glanceclient >= 2.8.0
Requires:         python2-heatclient >= 1.10.0
Requires:         python2-iso8601 >= 0.1.11
Requires:         python2-jinja2 >= 2.8
Requires:         python2-jsonschema >= 2.6.0
Requires:         python2-keystoneauth1 >= 3.3.0
Requires:         python2-keystoneclient >= 1:3.8.0
Requires:         python2-keystonemiddleware >= 4.17.0
Requires:         python2-manilaclient >= 1.16.0
Requires:         python2-neutronclient >= 6.3.0
Requires:         python2-novaclient >= 9.1.0
Requires:         python2-oslo-concurrency >= 3.25.0
Requires:         python2-oslo-config >= 2:5.1.0
Requires:         python2-oslo-context >= 2.19.2
Requires:         python2-oslo-db >= 4.27.0
Requires:         python2-oslo-i18n >= 3.15.3
Requires:         python2-oslo-log >= 3.36.0
Requires:         python2-oslo-messaging >= 5.29.0
Requires:         python2-oslo-middleware >= 3.31.0
Requires:         python2-oslo-policy >= 1.30.0
Requires:         python2-oslo-rootwrap >= 5.8.0
Requires:         python2-oslo-serialization >= 2.18.0
Requires:         python2-oslo-service >= 1.24.0
Requires:         python2-oslo-utils >= 3.33.0
Requires:         python2-paramiko >= 2.0
Requires:         python2-pbr >= 2.0.0
Requires:         python2-requests >= 2.14.2
Requires:         python2-six >= 1.10.0
Requires:         python2-sqlalchemy >= 1.0.10
Requires:         python2-stevedore >= 1.20.0
Requires:         python2-swiftclient >= 3.2.0
Requires:         python2-tooz >= 1.58.0
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


%package image-pack
Summary:          Sahara Image Pack

Requires:         python-sahara = %{epoch}:%{version}-%{release}
Requires:         python-libguestfs

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
%{__python2} setup.py build


%if 0%{?with_doc}
# Note: json warnings likely resolved w/ pygments 1.5 (not yet in Fedora)
sphinx-build -b html doc/source doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo}
sphinx-build -b man doc/source doc/build/man
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
export DISCOVER_DIRECTORY=sahara/tests/unit
%{__python2} setup.py test

%changelog
* Tue Sep 04 2018 RDO <dev@lists.rdoproject.org> 1:8.0.2-1
- Update to 8.0.2

* Tue May 15 2018 RDO <dev@lists.rdoproject.org> 1:8.0.1-1
- Update to 8.0.1

* Wed Feb 28 2018 RDO <dev@lists.rdoproject.org> 1:8.0.0-1
- Update to 8.0.0

* Thu Feb 15 2018 RDO <dev@lists.rdoproject.org> 1:8.0.0-0.1.0rc1
- Update to 8.0.0.0rc1
