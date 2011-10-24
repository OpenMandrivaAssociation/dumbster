# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Summary:        Fake SMTP Server
Name:           dumbster
Version:        1.6
Release:        11
License:        ASL 2.0
URL:            http://quintanasoft.com/dumbster/
Group:          Development/Java 
# cvs -z3 -d:pserver:anonymous@dumbster.cvs.sourceforge.net:/cvsroot/dumbster export -r RELEASE_1_6 dumbster
# tar czf dumbster-1.6-src.tgz dumbster
Source0:        %{name}-%{version}-src.tgz
Source1:        %{name}-1.6.pom
Patch0:         %{name}-SimpleSmtpServer.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  javamail
BuildRequires:  junit
Requires:       java-sasl
Requires:       javamail

BuildArch:      noarch

%description
The Dumbster is a very simple fake SMTP server designed for
unit and system testing applications that send email messages.
It responds to all standard SMTP commands but does not deliver
messages to the user. The messages are stored within the
Dumbster for later extraction and verification.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java 

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;

%patch0 -p0
rm -f src/com/dumbster/smtp/SimpleSmtpServer.java.orig

%build
pushd lib
ln -sf $(build-classpath javamail)
ln -sf $(build-classpath junit)
ln -sf $(build-classpath sasl)
popd

ant jar javadoc

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}

install -m 0644 build/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -dm 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
cp -pr %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP-%{name}.pom
%add_to_maven_depmap dumbster %{name} 1.6 JPP %{name}

install -dm 755 $RPM_BUILD_ROOT%{_javadir}/maven2
ln -s %{_datadir}/maven2/poms $RPM_BUILD_ROOT%{_javadir}/maven2/poms

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc license.txt
%{_javadir}/*.jar
%{_datadir}/maven2/poms
%{_javadir}/maven2
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

