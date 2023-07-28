Name:           glslang
Version:        12.2.0
Release:        1
Summary:        OpenGL and OpenGL ES shader front end and validator

License:        BSD and GPLv3+ and ASL 2.0
URL:            https://github.com/KhronosGroup/glslang
Source0:        %{name}-%{version}.tar.gz
Patch1:         glslang-default-resource-limits_staticlib.patch
# Patch to build against system spirv-tools (rebased locally)
#Patch2:         https://patch-diff.githubusercontent.com/raw/KhronosGroup/glslang/pull/1722.patch#/0001-pkg-config-compatibility.patch
Patch2:         0001-pkg-config-compatibility.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja
BuildRequires:  python3-base
#BuildRequires:  spirv-tools-devel

%description
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
%{name} is the official reference compiler front end for the OpenGL
ES and OpenGL shading languages. It implements a strict
interpretation of the specifications for these languages.

%prep
%autosetup -p1 -n %{name}-%{version}/%{name}
# Fix rpmlint warning on debuginfo
find . -name '*.h' -or -name '*.cpp' -or -name '*.hpp'| xargs chmod a-x

%build
%cmake -DBUILD_SHARED_LIBS=OFF
%make_build

%install
%make_install

# we don't want them in here
rm -rf %{buildroot}%{_includedir}/SPIRV

# Install libglslang-default-resource-limits.a
install -pm 0644 glslang/libglslang-default-resource-limits.a %{buildroot}%{_libdir}/

install -pm 0644 hlsl/libHLSL.a %{buildroot}%{_libdir}/
install -pm 0644 OGLCompilersDLL/libOGLCompiler.a %{buildroot}%{_libdir}/
install -pm 0644 glslang/libglslang.a %{buildroot}%{_libdir}/
install -pm 0644 glslang/libMachineIndependent.a %{buildroot}%{_libdir}/
install -pm 0644 glslang/OSDependent/Unix/libOSDependent.a %{buildroot}%{_libdir}/
install -pm 0644 glslang/libGenericCodeGen.a %{buildroot}%{_libdir}/
install -pm 0644 SPIRV/libSPVRemapper.a %{buildroot}%{_libdir}/
install -pm 0644 SPIRV/libSPIRV.a %{buildroot}%{_libdir}/

%files
%doc README.md README-spirv-remap.txt
%{_bindir}/glslangValidator
%{_bindir}/spirv-remap

%files devel
%{_includedir}/glslang/
%{_libdir}/libHLSL.a
%{_libdir}/libOGLCompiler.a
%{_libdir}/libOSDependent.a
%{_libdir}/libSPIRV.a
%{_libdir}/libSPVRemapper.a
%{_libdir}/libglslang.a
%{_libdir}/libGenericCodeGen.a
%{_libdir}/libMachineIndependent.a
%{_libdir}/libglslang-default-resource-limits.a
%{_libdir}/pkgconfig/glslang.pc
%{_libdir}/pkgconfig/spirv.pc
%{_libdir}/cmake/*
