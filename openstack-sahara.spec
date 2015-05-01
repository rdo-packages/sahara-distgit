#######################
# Globals Declaration #
#######################

%global release_name kilo
%global service sahara
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sahara_user sahara
%global sahara_group %{sahara_user}

%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}}
%endif

####################
# openstack-sahara #
####################

Name:          openstack-sahara
Version:       2015.1.0
Release:       1%{?milestone}%{?dist}
Provides:      openstack-savanna = %{version}-%{release}
Summary:       Apache Hadoop cluster management on OpenStack
License:       ASL 2.0
URL:           https://launchpad.net/sahara
Source0:       http://launchpad.net/%{service}/%{release_name}/%{version}/+download/%{service}-%{upstream_version}.tar.gz
Source1:       sahara.conf.sample
Source2:       openstack-sahara-all.service
Source3:       openstack-sahara-api.service
Source4:       openstack-sahara-engine.service
BuildArch:     noarch

#
# patches_base=%{version}%{?milestone}
#

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-sphinx >= 1.1.2
BuildRequires:    python-oslo-sphinx >= 2.5.0
BuildRequires:    python-sphinxcontrib-httpdomain
BuildRequires:    python-pbr >= 0.5.19
BuildRequires:    systemd-units

Requires:         openstack-sahara-common = %{version}-%{release}
Requires:         openstack-sahara-engine = %{version}-%{release}
Requires:         openstack-sahara-api = %{version}-%{release}

%description
Sahara provides the ability to elastically manage Apache Hadoop clusters on
OpenStack.

%files
%{_unitdir}/openstack-sahara-all.service
%{_bindir}/sahara-all

%post
%systemd_post openstack-sahara-all.service

%preun
%systemd_preun openstack-sahara-all.service

%postun
%systemd_postun_with_restart openstack-sahara-all.service

####################
# openstack-common #
####################

%package common
Summary:          Components common to all Sahara services

Requires:         python-alembic >= 0.6.4
#?Babel>=1.3?
Requires:         python-cinderclient >= 1.0.9
Requires:         python-eventlet >= 0.15.1
Requires:         python-flask >= 0.10
Requires:         python-heatclient >= 0.2.9
Requires:         python-iso8601 >= 0.1.9
Requires:         python-jinja2
Requires:         python-jsonschema >= 2.0.0
Requires:         python-keystoneclient >= 0.10.0
Requires:         python-keystonemiddleware >= 1.0.0
Requires:         python-neutronclient >= 2.3.6
Requires:         python-novaclient >= 2.18.0
Requires:         python-oslo-concurrency
Requires:         python-oslo-config >= 1.4.0
Requires:         python-oslo-context
Requires:         python-oslo-db >= 0.4.0
Requires:         python-oslo-i18n >= 0.3.0
Requires:         python-oslo-log
Requires:         python-oslo-messaging >= 1.4.0
Requires:         python-oslo-middleware
Requires:         python-oslo-policy
Requires:         python-oslo-rootwrap
Requires:         python-oslo-serialization >= 0.3.0
Requires:         python-oslo-utils
Requires:         python-paramiko >= 1.10.0
Requires:         python-pbr >= 0.5.19
Requires:         python-requests >= 1.2.1
Requires:         python-six >= 1.7.0
Requires:         python-sqlalchemy
Requires:         python-stevedore >= 0.14
Requires:         python-swiftclient >= 2.1.0
Requires:         python-webob >= 1.2.3

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

%description common
Sahara provides the ability to elastically manage Apache Hadoop clusters on
OpenStack. These components are common to all Sahara services.

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
%doc README.rst LICENSE
%dir %{_sysconfdir}/sahara
# Note: this file is not readable because it holds auth credentials
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/sahara.conf
%config(noreplace) %attr(-, root, %{sahara_group}) %{_sysconfdir}/sahara/policy.json
%{_bindir}/sahara-all
%{_bindir}/sahara-api
%{_bindir}/sahara-engine
%{_bindir}/_sahara-subprocess
%{_bindir}/sahara-db-manage
%{_bindir}/sahara-rootwrap
%{_bindir}/sahara-templates
%dir %attr(-, %{sahara_user}, %{sahara_group}) %{_sharedstatedir}/sahara
%dir %attr(0750, %{sahara_user}, %{sahara_group}) %{_localstatedir}/log/sahara
# Note: permissions on sahara's home are intentionally 0700
%dir %{_datadir}/sahara
%{_datadir}/sahara/sahara.conf.sample
%{python2_sitelib}/sahara
%{python2_sitelib}/sahara-%{version}*-py?.?.egg-info

#################
# openstack-doc #
#################

%package doc
Group:         Documentation
Summary:       Usage documentation for the Sahara cluster management API
Requires:      %{name} = %{version}

%description doc
Sahara provides the ability to elastically manage Apache Hadoop clusters on
OpenStack. This documentation provides instructions and examples on how to
install, use, and manage the Sahara infrastructure.

%files doc
%{_pkgdocdir}/html

####################
# openstack-engine #
####################

%package engine
Summary:          The Sahara cluster management engine

Requires:         openstack-sahara-common = %{version}-%{release}

%description engine
Sahara provides the ability to elastically manage Apache Hadoop clusters on
OpenStack. This documentation provides instructions and examples on how to
install, use, and manage the Sahara infrastructure.

%files engine
%{_unitdir}/openstack-sahara-engine.service
%{_bindir}/sahara-engine

%post engine
%systemd_post openstack-sahara-engine.service

%preun engine
%systemd_preun openstack-sahara-engine.service

%postun engine
%systemd_postun_with_restart openstack-sahara-engine.service

#################
# openstack-api #
#################

%package api
Summary:          The Sahara cluster management API

Requires:         openstack-sahara-common = %{version}-%{release}

%description api
Sahara provides the ability to elastically manage Apache Hadoop clusters on
OpenStack. This documentation provides instructions and examples on how to
install, use, and manage the Sahara infrastructure.

%files api
%{_unitdir}/openstack-sahara-api.service
%{_bindir}/sahara-api

%post api
%systemd_post openstack-sahara-api.service

%preun api
%systemd_preun openstack-sahara-api.service

%postun api
%systemd_postun_with_restart openstack-sahara-api.service

######################
# Common Build Steps #
######################

%prep
%setup -q -n sahara-%{upstream_version}

sed -i s/REDHAT_SAHARA_VERSION/%{version}/ sahara/version.py
sed -i s/REDHAT_SAHARA_RELEASE/%{release}/ sahara/version.py

sed -i 's/%{version}/%{version}/' PKG-INFO

rm -rf sahara.egg-info
rm -f test-requirements.txt
cp %{SOURCE1} etc/sahara/sahara.conf.sample
# The data_files glob appears broken in pbr 0.5.19, so be explicit
sed -i 's,etc/sahara/\*,etc/sahara/sahara.conf.sample,' setup.cfg
# remove the shbang from these files to supress rpmlint warnings, these are
# python based scripts that get processed to form the installed shell scripts.
sed -i 1,2d sahara/cli/sahara_all.py
sed -i 1,2d sahara/cli/sahara_api.py
sed -i 1,2d sahara/cli/sahara_engine.py
sed -i 1,2d sahara/cli/sahara_subprocess.py
# set executable on these files to supress rpmlint warnings, they are used as
# templates to create shell scripts.
chmod a+x sahara/plugins/vanilla/hadoop2/resources/post_conf.template
chmod a+x sahara/plugins/spark/resources/spark-env.sh.template
# also set executable on this topology script, should have been set upstream
chmod a+x sahara/plugins/spark/resources/topology.sh

%build
%{__python2} setup.py build

export PYTHONPATH=$PWD:${PYTHONPATH}
# Note: json warnings likely resolved w/ pygments 1.5 (not yet in Fedora)
sphinx-build doc/source html
rm -rf html/.{doctrees,buildinfo}


%install
%{__python2} setup.py install --skip-build --root %{buildroot}

install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-sahara-all.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-sahara-api.service
install -p -D -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/openstack-sahara-engine.service

HOME=%{_sharedstatedir}/sahara
install -d -m 700 %{buildroot}$HOME

SAMPLE=%{buildroot}%{_datadir}/sahara/sahara.conf.sample
CONF=%{buildroot}%{_sysconfdir}/sahara/sahara.conf
install -d -m 755 $(dirname $CONF)
install -D -m 640 $SAMPLE $CONF
install -D -m 640 etc/sahara/policy.json %{buildroot}%{_sysconfdir}/sahara/policy.json

# Do not package tests
rm -rf %{buildroot}%{python2_sitelib}/sahara/tests

mkdir -p -m0755 %{buildroot}/%{_localstatedir}/log/sahara

# Copy built doc files for doc subpackage
mkdir -p %{buildroot}/%{_pkgdocdir}
cp -rp html %{buildroot}/%{_pkgdocdir}

%check
# Building on koji with virtualenv requires test-requirements.txt and this
# causes errors when trying to resolve the package names, also turning on pep8
# results in odd exceptions from flake8.
# sh run_tests.sh --no-virtual-env --no-pep8

#############
# Changelog #
#############

%changelog
* Fri May 01 2015 Ethan Gafford <egafford@redhat.com> 2015.1.0-1
- Update to upstream 2015.1.0

* Wed Apr 29 2015 Ethan Gafford <egafford@redhat.com> 2015.1-0.2.0rc2
- Removing patches unnecessary per kilo guidelines

* Wed Apr 29 2015 Ethan Gafford <egafford@redhat.com> 2015.1-0.1.0rc2
- Update to version tracking for Fedora and Delorean compatibility

* Thu Apr 23 2015 Ethan Gafford <egafford@redhat.com> 2015.1.0rc2-1
- Update to upstream 2015.1.0rc2

* Mon Mar 23 2015 Ethan Gafford <egafford@redhat.com> 2014.2.2-4
- Added launch_command.py to MANIFEST.in
- Resolves: rhbz#1184522
- Downgraded most dependencies for older Fedora compatibility
- Removed pre-systemd packaging apparatus

* Fri Mar 20 2015 Ethan Gafford <egafford@redhat.com> 2014.2.2-3
- Updated dependencies from upstream requirements.txt

* Thu Mar 19 2015 Ethan Gafford <egafford@redhat.com> 2014.2.2-2
- Updated with patches from RDO patches branch (no-op change)

* Thu Feb 05 2015 Ethan Gafford <egafford@redhat.com> 2014.2.2-1
- Update to upstream 2014.2.2

* Tue Dec 09 2014 Ethan Gafford <egafford@redhat.com> 2014.2.1-2
- Removed sed replacement of default connection in /etc/sahara/sahara.conf
- Resolves rhbz#1162304

* Tue Dec 09 2014 Ethan Gafford <egafford@redhat.com> 2014.2.1-1
- Update to upstream 2014.2.1
- Changing log directory permissions to 0750.

* Fri Oct 17 2014 Michael McCune <mimccune@redhat.com> 2014.2
- Juno release

* Tue Oct 07 2014 Michael McCune <mimccune@redhat.com> 2014.2-0.3.rc2
- Update to upstream 2014.2.rc2

* Tue Oct 07 2014 Michael McCune <mimccune@redhat.com> 2014.2-0.2.rc1
- updating dependencies

* Thu Oct 02 2014 Michael McCune <mimccune@redhat.com> 2014.2-0.1.rc1
- Update to upstream 2014.2.rc1

* Wed Sep 24 2014 Michael McCune <mimccune@redhat.com> 2014.2-0.4.b3
- Bug fixes to upstream 2014.2.b3
- Resolves: rhbz#1144529
- Resolves: rhbz#1144531
- adding patch to fix keystonemiddleware==1.0.0 issues

* Tue Sep 16 2014 Michael McCune <mimccune@redhat.com> - 2014.2-0.3.b3
- spec cleanup

* Tue Sep 16 2014 Michael McCune <mimccune@redhat.com> - 2014.2-0.2.b3
- juno-3 milestone

* Wed Jul 30 2014 Michael McCune <mimccune@redhat.com> - 2014.2-0.2.b2
- juno-2 milestone

* Thu Jul 17 2014 Pádraig Brady <pbrady@redhat.com> - 2014.1.1-1
- Stable icehouse 2014.1.1 rebase

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2014.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 07 2014 Michael McCune <mimccune@redhat> - 2014.1.0-13
- Adding missing shell scripts to manifest patch

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 2014.1.0-12
- Patching MANIFEST.in for missing hdp plugin resources and alembic migrations
- Removing the cp for alembic migrations

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 2014.1.0-11
- Adding BuildRequire for python-sphinx

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 2014.1.0-10
- Removing pbr from Requires
- changing version and release temp from patch

* Mon May 05 2014 Michael McCune <mimccune@redhat> - 2014.1.0-9
- Adding patch to remove runtime pbr requirement

* Fri May 02 2014 Michael McCune <mimccune@redhat> - 2014.1.0-8
- Removing python-sqlalchemy and python-paste-deploy from BuildRequires
- refactoring the systemd portions

* Fri May 02 2014 Michael McCune <mimccune@redhat> - 2014.1.0-7
- Changing parallel build require for python-sqlalchemy0.7
- Removing chmod in post
- Replacing user/group in attrs with global variables

* Wed Apr 30 2014 Michael McCune <mimccune@redhat> - 2014.1.0-6
- Adding sahara user ownership to log dir
- Creating local variables for sahara user and group

* Wed Apr 30 2014 Michael McCune <mimccune@redhat> - 2014.1.0-5
- Adding alembic migration files, addressing BZ1094757

* Wed Apr 30 2014 Michael McCune <mimccune@redhat> - 2014.1.0-4
- Correcting bug with rhel6 init script, addressing BZ1094755
- Adding local variable for rhel6 tests

* Thu Apr 24 2014 Michael McCune <mimccune@redhat> - 2014.1.0-3
- merging in el6 spec, with conditionals

* Thu Apr 24 2014 Michael McCune <mimccune@redhat> - 2014.1.0-2
- adding _pkgdocdir macro for rhel<=7

* Tue Apr 22 2014 Michael McCune <mimccune@redhat> - 2014.1.0-1
- 2014.1 release

* Tue Apr 08 2014 Michael McCune <mimccune@redhat> - 2014.1.rc1-1
- 2014.1.rc1 release and rename from openstack-savanna

* Fri Mar 14 2014 Matthew Farrellee <matt@redhat> - 2014.1.b3-2
- Fixed python-webob dependency version

* Mon Mar 10 2014 Matthew Farrellee <matt@redhat> - 2014.1.b3-1
- 2014.1.b3 release

* Mon Jan 27 2014 Matthew Farrellee <matt@redhat> - 2014.1.b2-3
- Require stevedore >= 0.13

* Mon Jan 27 2014 Matthew Farrellee <matt@redhat> - 2014.1.b2-2
- Added space around paramiko requires

* Mon Jan 27 2014 Matthew Farrellee <matt@redhat> - 2014.1.b2-1
- 2014.1.b2 release

* Sat Jan 18 2014 Matthew Farrellee <matt@redhat> - 2014.1.b1-1
- 2014.1.b1 release

* Tue Oct 22 2013 Matthew Farrellee <matt@redhat> - 0.3-3
- Include Vanilla Plugin SQL files (for EDP)

* Tue Oct 22 2013 Matthew Farrellee <matt@redhat> - 0.3-2
- Fix db connection url

* Sun Oct 20 2013 Matthew Farrellee <matt@redhat> - 0.3-1
- 0.3 release
- Enable logging into /var/log/savanna

* Fri Oct 11 2013 Matthew Farrellee <matt@redhat> - 0.3-0.2
- 0.3 rc3 build

* Mon Aug 12 2013 Matthew Farrellee <matt@redhat> - 0.2-3
- Updates to build on F19,
-  Require systemd-units, allows mockbuild to work
-  Remove setuptools-git from setup.py, no downloads during build

* Fri Aug 09 2013 Matthew Farrellee <matt@redhat> - 0.2-2
- Updates from package review BZ986615

* Mon Jul 15 2013 Matthew Farrellee <matt@redhat> - 0.2-1
- Initial package
